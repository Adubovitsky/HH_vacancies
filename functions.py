
import json
import requests

class vacancies_class:
    """
    В данный объект выргужаются с сайта данные о вакансиях по заданным пораметрам и затем с помощью методов класса

    """

    def __init__(self, url, text, area):
        self.url = url
        self.text = text
        self.area = area
        self.salary = True
        self.mean_salary = None
        self.count = None
        self.result = {}
        self.skills_and_freq = {}
        self.requirements = []


    def get_vacancies(self):
        """
        Функция формирует первичный список данных по вакансиям на основании параметров запроса
        :param text:
        :param area:
        :param with_salary:
        :return:
        """

        my_params1 = {
                'page': 1,
                'text': self.text,
                "area": self.area,
                'only_with_salary': self.salary
            }
        result = requests.get(self.url, params=my_params1).json()
        self.count = result["found"]
        return result

    def get_vacancies_all_pages(self):
        """
        Так как в ответе на запрос от сайта за один раз передается только одна страница, данная функция обходит все страницы
        чтобы сформировать единый полный лист вакансий
        :return:
        """
        full_list = []
        for i in range(self.count // 20 + 1):
            my_params = {
                'page': i,
                'text': self.text,
                "area": self.area,
                'only_with_salary': self.salary
            }
            result = requests.get(self.url, params=my_params).json()
            items_on_page = result["items"]
            full_list+=items_on_page
        return full_list

    def get_list_url(self,full_vacancies_list):
        """
        Функция формирует список сайтов api url
        :param vacacies_list:
        :return:
        """
        list_url = []
        for i in full_vacancies_list:
            url = i["url"]
            list_url.append(url)
        return list_url

    def request_api_url(self,list):
        """
        Функция обходит сайты api_url и формирует список данных, находящихся на этих сайтах
        :param list: список url вдресов сайтов выбранных вакансий
        :return:
        """
        vacancies_from_api_url = []
        for i in list:
            result = requests.get(i).json()
            vacancies_from_api_url.append(result)
        return vacancies_from_api_url

    def get_list_of_key_skills_lists(self, vacancies_from_api):
        """
        Функция обходит в цикле вакасии, полученные с api url, находит в них списки key_skills и объединяет их в общий список
        В результате получается список, состоящий из других списков
        :param vacancies_from_api:
        :return:
        """
        new_list = []
        for i in vacancies_from_api:
            key_skills = i["key_skills"]
            new_list.append(key_skills)
        return new_list

    def get_list_of_skills(self, list):
        """
        Фукция формирует простой список требуемых навыков из формата списка, состоящего из списка словарей
        :param list:
        :return:
        """
        new_list = []
        for i in list:
            for j in i:
                key_skills = j["name"]
                new_list.append(key_skills)
        return new_list

    def calculate_frequency_of_required_skills(self,list):
        """
        Фуккция рассчитывает, в скольких вакансиях встретился каждый навык и формирует словарь {"название навыка": количество упоминаний}
        :param list:
        :return:
        """
        new_dict = {}
        set_skills = set(list)
        for i in set_skills:
            new_dict[i]= list.count(i)
            self.skills_and_freq = new_dict
        return self.skills_and_freq

    def make_requirements_list(self):
        """
        Фукция формирует список  словарей с данными о навыках, при этом словари сортируются по значению "count" по убыванию
        :return:
        """
        new_list = []
        dict = {}
        for i in self.skills_and_freq.keys():
            dict["name"]=i
            dict["count"]=self.skills_and_freq[i]
            dict["percent"] = round(self.skills_and_freq[i]/self.count*100,1)
            dict1 = dict.copy()
            new_list.append(dict1)
        self.requirements = sorted(new_list,key=lambda d: d["count"], reverse=True)
        return self.requirements

    def __str__(self):
        self.result["keywords"] = self.text
        self.result["count"] = self.count
        self.result ["average salary, RUR"] = self.mean_salary
        self.result["requirements"] = self.requirements
        return json.dumps(self.result,ensure_ascii=False,indent=4)


    def calculate_average_salary(self,vacancies_list):
        """
        Функция рассчитывает среднюю заработную плату по данным вакансий
        :param vacancies_list:
        :return:
        """
        cumulative_mean_salary = 0
        quantity_of_vacancies = len(vacancies_list)
        for i in vacancies_list:
            min_salary = i["salary"]["from"]
            max_salary = i["salary"]["to"]
            currency = i["salary"]["currency"]
            gross = i["salary"]["gross"]
            mean_salary = None
            Euro_exchange_rate = 66
            Dollar_exchage_rate = 63
            if currency in ["RUR",None]:
                if min_salary:
                    if max_salary:
                        mean_salary = (min_salary+max_salary)/2
                    else:
                        mean_salary = min_salary
                else:
                    mean_salary = max_salary
            elif currency == "EUR":
                if min_salary:
                    if max_salary:
                        mean_salary = (min_salary+max_salary)/2*Euro_exchange_rate
                    else:
                        mean_salary = min_salary*Euro_exchange_rate
                else:
                    mean_salary = max_salary*Euro_exchange_rate
            elif currency == "USD":
                if min_salary:
                    if max_salary:
                        mean_salary = (min_salary+max_salary)/2*Dollar_exchage_rate
                    else:
                        mean_salary = min_salary*Dollar_exchage_rate
                else:
                    mean_salary = max_salary*Dollar_exchage_rate
            gross_mean_salary = mean_salary if gross else mean_salary/0.87
            cumulative_mean_salary += gross_mean_salary
            self.mean_salary = round(cumulative_mean_salary/quantity_of_vacancies,2)
        return self.mean_salary


