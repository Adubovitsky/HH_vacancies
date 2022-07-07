from flask import Flask, render_template, request
import json
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
    experience = request.form['experience']
    url = 'https://api.hh.ru/vacancies'
    vacancies = vacancies_class(url, job, area, experience)
    vacancies.get_vacancies()
    full_list = vacancies.get_vacancies_all_pages()
    vacancies.calculate_average_salary(full_list)
    list_url = vacancies.get_list_url(full_list)
    vacancies_data_from_api = vacancies.request_api_url(list_url)
    listoflist_key_skills = vacancies.get_list_of_key_skills_lists(vacancies_data_from_api)
    key_skills = vacancies.get_list_of_skills(listoflist_key_skills)
    vacancies.calculate_frequency_of_required_skills(key_skills)
    vacancies.make_requirements_list()
    result = vacancies.make_result()
    skills = result["requirements"]
    return render_template("output.html", job=job, area=area, result=result, skills=skills, area_dict=area_dict)


if __name__ == "__main__":
    app.run(debug=True)


