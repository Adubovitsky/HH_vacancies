
import json
from functions import vacancies_class

DOMAIN = 'https://api.hh.ru/'
url_vacancies = f'{DOMAIN}vacancies'

job = input("Введите название вакансии или ключевые слова для поиска ")

while True:
    area_request = input("Введите регион поиска: 1 - Москва, 2- Санкт-Петербург, 3 - Екатеринбург, 113 - Вся Россия ")
    if area_request in ["1","2","3","113"]:
        area = int(area_request)
        break
    else:
        print("Неправильно указан регион поиска вакансии. Введите регион еще раз")

vacancies = vacancies_class(url_vacancies,job,area)
vacancies.get_vacancies()

print("Подождите идет обработка запроса...")

full_list = vacancies.get_vacancies_all_pages()
vacancies.calculate_average_salary(full_list)

list_url = vacancies.get_list_url(full_list)
vacancies_data_from_api = vacancies.request_api_url(list_url)
listoflist_key_skills = vacancies.get_list_of_key_skills_lists(vacancies_data_from_api)
key_skills = vacancies.get_list_of_skills(listoflist_key_skills)
vacancies.calculate_frequency_of_required_skills(key_skills)
vacancies.make_requirements_list()
print(vacancies)

with open("vacancies.json", "w") as f:
    json.dump(vacancies.result,f, ensure_ascii=False, indent=4)
















# url_vacancies = 'https://api.hh.ru/vacancies'
# params = {
#     'text': "Финансовый директор",
#     'page':1
# }
#
# result = requests.get(url_vacancies,params=params).json()
#
# items = result["items"]
# first = items[0]
# # pprint.pprint(first)
#
# pprint.pprint(first['alternate_url'])
# pprint.pprint(first['url'])
# one_vacancy = first['url']
#
# result = requests.get(one_vacancy,params=params).json()
# pprint.pprint(result)