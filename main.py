from flask import Flask, render_template, request
from sqlalchemy import create_engine
from functions import vacancies_class
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from alchemy import Vacancies, Areas, Employers
from datetime import date, datetime, timedelta

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
    dateform = request.form['date']

    if dateform == "today":
        date_from = date.today()
    elif dateform == "last_7days":
        date_from = date.today()-timedelta(days=7)
    elif dateform == "last_14days":
        date_from = date.today()-timedelta(days=14)
    else:
        date_from = date.today() - timedelta(days=29)

    url = 'https://api.hh.ru/vacancies'
    vacancies = vacancies_class(url, job, area, date_from)
    vacancies.get_vacancies()
    full_list = vacancies.get_vacancies_all_pages()
    list_url = vacancies.get_list_url(full_list)
    vacancies_data_from_api = vacancies.request_api_url(list_url)
    key_data = vacancies.key_data_api(vacancies_data_from_api)
    count= vacancies.count

    engine = create_engine('sqlite:///hhalchem1.sdb', echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Vacancies).delete()
    session.query(Employers).delete()
    session.commit()

    for i in key_data:
        vac = Vacancies(i['id'], i['area_id'], i['employer_id'], i['experience'], i['published_at'], i['link'],
                        i['name'], i['metro'], i['street'], i['mean_salary'])
        session.add(vac)
        try:
            emp = Employers(i['employer_name'], i['employer_id'], i['employer_link'])
            session.add(emp)
            session.commit()
        except IntegrityError:
            session.rollback()

    session.commit()

    vac_list=[]
    query = session.query(Vacancies, Employers, Areas).select_from(Vacancies).join(Employers).join(Areas).order_by(Vacancies.salary.desc()).all()
    for v, e, ar in query:
        dict={}
        dict['name']=v.name
        dict['emp'] = e.name
        dict['sal'] = v.salary
        dict['city'] = ar.name
        dict['str'] = v.street
        dict['met'] = v.metro
        dict['date'] = v.published_at
        dict['link'] = v.link
        vac_list.append(dict)

    return render_template("output.html", job=job, area=area, vac_list=vac_list, area_dict=area_dict, count=count)

if __name__ == "__main__":
    app.run(debug=True)


