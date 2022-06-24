from flask import Flask, render_template, request
import sqlite3
from functions import vacancies_class

app = Flask(__name__)

area_dict={"Санкт_Петербург":2,"Екатеринбург":3, "Новосибирск":4,"Москва":1,"Нижний Новгород":66,
              "Красноярск":54,"Иркутск":35,"Воронеж":26,"Казань":88,"Краснодар":53,"Ростов на Дону":76,
              "Самара":78,"Уфа":99,"Пермь":72,"Сочи":237}

@app.route("/")
def index():
   return render_template("Index.html")

@app.route("/form/", methods=['GET'])
def form_get():
   return render_template("form.html", area_dict=area_dict)

@app.route("/contacts/")
def contacts():
    telephone_number = "+7 999 999 99 99"
    address = "Москва, ул. Шаболовская 38"
    email = "info@smartsearch.com"
    return render_template("contacts.html", phone = telephone_number, address = address, email=email)

@app.route("/output/", methods=['GET'])
def output_get():
    result={}
    return render_template("output.html", result=result)

@app.route("/output/", methods=['POST'])
def output_post():
    job = request.form['job']
    area = int(request.form['area'])

    url = 'https://api.hh.ru/vacancies'
    vacancies = vacancies_class(url, job, area)
    vacancies.get_vacancies()
    full_list = vacancies.get_vacancies_all_pages()
    list_url = vacancies.get_list_url(full_list)
    vacancies_data_from_api = vacancies.request_api_url(list_url)
    key_data = vacancies.key_data_api(vacancies_data_from_api)
    salary = vacancies.get_salary(vacancies_data_from_api)
    count= vacancies.count

    conn = sqlite3.connect('hh.sdb')
    cursor = conn.cursor()

    cursor.execute('DELETE from address')
    cursor.execute('DELETE from Employers')
    cursor.execute('DELETE from salary ')
    cursor.execute('DELETE from Vacancies ')
    conn.commit()

    for i in key_data:
        cursor.execute(
            "insert INTO Vacancies (hh_id, area_id, employer_id, experience, published_at, link, name, street, metro) VALUES (?,?,?,?,?,?,?,?,?)",
            (i['id'], i['area_id'], i['employer_id'], i['experience'], i['published_at'], i['link'], i['name'], i['street'], i['metro']))

        cursor.execute(
            "insert INTO Employers (emp_hhid, name, link_employer) VALUES (?,?,?)",
            (i['employer_id'], i['employer_name'], i['employer_link']))

    for i in salary:
        cursor.execute(
            "insert INTO salary (hh_id, salary_from, salary_to, currency, gross, salary) VALUES (?,?,?,?,?,?)",
            (i['id'], i['min_salary'], i['max_salary'], i['currency'], i['gross'], i['mean_salary']))

    conn.commit()

    query2 = 'select  v.name, e.name,  s.salary, a.name, v.street, v.metro, v.link from Vacancies v, salary s, Employers e, areas a' \
             '  where v.hh_id=s.hh_id and v.employer_id = e.emp_hhid and v.area_id = a.hh_id'


    cursor.execute(query2)
    result = cursor.fetchall()


    return render_template("output.html", job=job, area=area, result=result, area_dict=area_dict, count=count)


if __name__ == "__main__":
    app.run(debug=True)


