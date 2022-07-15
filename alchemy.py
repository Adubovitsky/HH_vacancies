from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import json


engine = create_engine('sqlite:///hhalchem1.sdb', echo=True)

Base = declarative_base()

class Vacancies(Base):
    __tablename__ = 'vacancies'
    hh_id = Column(String, primary_key=True)
    area_id = Column(String, ForeignKey('areas.hh_id'))
    employer_id = Column(String, ForeignKey('employers.emp_hhid') )
    experience = Column(String)
    published_at = Column(String(10))
    link = Column(String)
    name = Column(String)
    metro = Column(String)
    street = Column(String)
    salary = Column(Integer)

    def __init__(self, hh_id, area_id, employer_id, experience, published_at, link, name, metro, street, salary):
        # self.id = id
        self.hh_id = hh_id
        self.area_id = area_id
        self.employer_id = employer_id
        self.experience = experience
        self.published_at = published_at
        self.link = link
        self.name = name
        self.metro = metro
        self.street = street
        self.salary = salary


    def __str__(self):
        return f'{self.id}) {self.name}'

class Employers(Base):
    __tablename__ = 'employers'
    name = Column(String)
    emp_hhid = Column(String, primary_key=True)
    link_employer = Column(String)


    def __init__(self, name, emp_hhid, link_employer):
        self.name = name
        self.emp_hhid = emp_hhid
        self.link_employer = link_employer

    def __str__(self):
        return f'{self.id}) {self.name}'


class Areas(Base):
    __tablename__ = 'areas'

    name = Column(String)
    hh_id = Column(String, primary_key=True)
    parent_id = Column(String, nullable=True)

    def __init__(self, name, hh_id, parent_id):
        self.name = name
        self.hh_id = hh_id
        self.parent_id = parent_id

    def __str__(self):
        return f'{self.id}) {self.name}'

Base.metadata.create_all(engine)








# Session = sessionmaker(bind=engine)
# session = Session()



# query = session.query(Vacancies, Employers, Areas).select_from(Vacancies).join(Employers).join(Areas).order_by(Vacancies.salary.desc()).all()
# for i, j, y in query:
#     print(i.name, i.salary, j.name, y.name)
#
# query = session.query(Vacancies)
# for i in query:
#     print(i.published_at)





#
# f = open('vacancies.json', 'r')
# data = json.loads(f.read())
#
# for i in data:
#     vac = Vacancies(i['id'], i['area_id'], i['employer_id'], i['experience'], i['published_at'], i['link'],i['name'], i['metro'], i['street'], i['mean_salary'] )
#     session.add(vac)
#     try:
#         emp = Employers(i['employer_name'], i['employer_id'],i['employer_link'] )
#         session.add(emp)
#         session.commit()
#     except IntegrityError:
#         session.rollback()
#
# session.commit()
#
#
#
# g = open('areas.json', 'r', encoding='utf8')
# areas = json.loads(g.read())
#
# for i in areas:
#     try:
#         area = Areas(i['name'], i['id'], i['parent_id'])
#         session.add(area)
#         session.commit()
#     except IntegrityError:
#         session.rollback()