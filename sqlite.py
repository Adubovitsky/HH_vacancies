import sqlite3

conn = sqlite3.connect('hh.sdb')
cursor = conn.cursor()

# cursor.execute('DELETE from address')
# cursor.execute('DELETE from salary ')
# conn.commit()

query = 'select  v.name, v.link, s.salary, a.street from Vacancies v, salary s, address a  where v.hh_id=s.hh_id'\
                        'and v.hh_id = a.hh_id'
query1 = 'select s.salary from  salary s '
query2 = 'select  v.name, v.link, s.salary, a.street, a.metro from Vacancies v, salary s, address a  where v.hh_id=s.hh_id and v.hh_id = a.hh_id'
query3 = 'select  v.name, e.name,  s.salary, v.street, v.metro, v.link from Vacancies v, salary s, Employers e  where v.hh_id=s.hh_id and v.hh_id = e.emp_hhid'
query4 = 'select  v.name,  s.salary, v.street, v.metro, v.link from Vacancies v, salary s  where v.hh_id=s.hh_id '
query5 = 'select  e.name, e.id, v.name from Employers e, Vacancies v where v.employer_id = e.emp_hhid  '


cursor.execute(query5)
result = cursor.fetchall()
print(result)

# cursor.execute('SELECT * from Vacancies where name=?', ('Director',))
# result = cursor.fetchall()
# print(result)