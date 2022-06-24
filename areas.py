import sqlite3
import requests


url = "https://api.hh.ru/areas"

result = requests.get(url).json()

areas_list=[]
for i in result:
    record = {}
    record["id"] = i["id"]
    record["name"] = i["name"]
    record["parent_id"] = i["parent_id"]
    areas_list.append(record)
    if i["areas"]:
        for j in range(len(i['areas'])):
            record1 = {}
            record1["id"] = i["areas"][j]["id"]
            record1["name"] = i["areas"][j]["name"]
            record1["parent_id"] = i["areas"][j]["parent_id"]
            areas_list.append(record1)
            if i["areas"][j]["areas"]:
                for y in range(len(i['areas'][j]['areas'])):
                    record2 = {}
                    record2["id"] = i["areas"][j]["areas"][y]["id"]
                    record2["name"] = i["areas"][j]["areas"][y]["name"]
                    record2["parent_id"] = i["areas"][j]["areas"][y]["parent_id"]
                    areas_list.append(record2)
print(areas_list)

conn = sqlite3.connect('hh.sdb')
cursor = conn.cursor()

for i in areas_list:
    cursor.execute("insert INTO Vacancies (name, hh_id, parent_id) VALUES (?,?,?)", (i['name'], i['id'], i['parent_id']))
conn.commit()
