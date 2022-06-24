
import json
import requests


class vacancies_class:
    """
    В данный объект выргужаются с сайта данные о вакансиях по заданным пораметрам и затем с помощью функций класса проводится аналитика данных вакансий

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
                'only_with_salary': self.salary,
                'per_page':100

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
        page_count = self.count//100+1
        if page_count>=20:
            page_count_adj=20
        else:
            page_count_adj = page_count

        for i in range(page_count_adj):
            my_params = {
                'page': i,
                'text': self.text,
                "area": self.area,
                'only_with_salary': self.salary,
                'per_page':100

            }
            result = requests.get(self.url, params=my_params).json()
            if result["items"]:
                items_on_page = result["items"]
                full_list+=items_on_page

            else:
                full_list=full_list
            # time.sleep(1)

        return full_list

    def get_list_url(self,full_vacancies_list):
        """
        Функция формирует список сайтов api url, на которых есть информация о требуемых навыках
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
            try:
                result = requests.get(i).json()
                vacancies_from_api_url.append(result)
                #print(i)
            except requests.exceptions.ConnectTimeout:
                print("timeout", i)
                continue

        return vacancies_from_api_url

    def key_data_api(self, vacancies_from_api):
        new_list=[]
        no_data = "не указано"
        for i in vacancies_from_api:
            record = {}
            record["id"] = i["id"] if "id" in i else no_data
            print(i['id'])
            record["name"] = i["name"]

            record["employer_id"] = i["employer"]["id"] if "id" in i['employer'] else no_data
            record["employer_name"] = i["employer"]["name"] if "name" in i['employer'] else no_data
            record["employer_link"] = i["employer"]["alternate_url"] if "alternate_url" in i['employer'] else no_data
            record["area_id"] = i["area"]["id"]
            record["published_at"] = i["published_at"]  if "published_at" in i else no_data
            record["link"] = i["alternate_url"] if "alternate_url" in i else no_data
            record["experience"] = i["experience"]["name"] if "experience" in i else no_data
            if i["address"] != None:
                record["street"] = i["address"]["street"] if i["address"]["street"] else no_data
                if i["address"]["metro"] != None:
                    record["metro"] = i["address"]["metro"]['station_name'] if i["address"]["metro"][
                        'station_name'] else no_data
                else:
                    record["metro"] = no_data
            else:
                record["street"] = 'не указано'
                record["metro"] = 'не указано'


            #
            # if i != None:
            #     record["id"] = i["id"] if "id" in i else no_data
            #     print(record['id'])
            #     record["name"] = i["name"] if "name" in i else no_data
            #     if "employer" in i:
            #         record["employer_id"] = i["employer"]["id"]
            #         record["employer_name"] = i["employer"]["name"] if i["employer"]["name"] else no_data
            #         if "alternate_url" not in i["employer"]:
            #             record["employer_link"]=no_data
            #         else:
            #             record["employer_link"] = i["employer"]["alternate_url"] if i["employer"]["alternate_url"] else no_data
            #     else:
            #         record["employer_id"]=no_data
            #
            #     record["area_id"] = i["area"]["id"] if "area" in i else no_data
            #     # record["description"] = i["description"]
            #     # record["experience"] = i["experience"]["name"]
            #     record["published_at"] = i["published_at"]  if 'published_at' in i else no_data
            #     record["link"] = i["alternate_url"]  if "link" in i else no_data
            #     if "address" in i:
            #         if i["address"] != None:
            #             record["street"] = i["address"]["street"] if i["address"]["street"] else no_data
            #             if i["address"]["metro"] != None:
            #                 record["metro"] = i["address"]["metro"]['station_name'] if i["address"]["metro"]['station_name'] else no_data
            #             else:
            #                 record["metro"]=no_data
            #         else:
            #             record["street"]='не указано'
            #             record["metro"] = 'не указано'
            #     else:
            #         record["street"] = 'странный случай'
            #         record["metro"] = 'странный случай'
            # else:
            #     pass

            # print(record['street'])

            new_list.append(record)

        return new_list

    def get_salary(self, vacancies_from_api):
        new_list = []
        for i in vacancies_from_api:
            record = {}
            no_data ="нет данных"
            record["id"] = i["id"]

            record["currency"] = i["salary"]["currency"] if i["salary"]["currency"] else no_data
            record["gross"] = i["salary"]["gross"] if i["salary"]["gross"] else no_data

            if i["salary"]["from"]:
                record["min_salary"] = i["salary"]["from"]
                if i["salary"]["to"]:
                    record["max_salary"] = i["salary"]["to"]
                    record["mean_salary"] = (i["salary"]["from"] + i["salary"]["to"]) / 2
                else:
                    record["max_salary"] = no_data
                    record["mean_salary"] = i["salary"]["from"]
            else:
                record["min_salary"] = no_data
                record["max_salary"] = i["salary"]["to"] if i["salary"]["to"] else no_data
                record["mean_salary"] = i["salary"]["to"] if i["salary"]["to"] else no_data
            new_list.append(record)
        return new_list


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

    def make_result(self):
        self.result["keywords"] = self.text
        self.result["count"] = self.count
        self.result ["average salary, RUR"] = self.mean_salary
        self.result["requirements"] = self.requirements
        return self.result

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
            Euro_exchange_rate = 60
            Dollar_exchage_rate = 55
            Tenge_exchage_rate = 0.12

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
            elif currency == "KZT":
                if min_salary:
                    if max_salary:
                        mean_salary = (min_salary+max_salary)/2*Tenge_exchage_rate
                    else:
                        mean_salary = min_salary*Tenge_exchage_rate
                else:
                    mean_salary = max_salary*Tenge_exchage_rate


            gross_mean_salary = mean_salary if gross else mean_salary/0.87
            #print(gross_mean_salary, min_salary, max_salary, currency, gross)
            cumulative_mean_salary += gross_mean_salary
            self.mean_salary = round(cumulative_mean_salary/quantity_of_vacancies,2)
        return self.mean_salary

    def get_address(self,full_vacancies_list):
        """
        Функция формирует основные нужные данные из списка вакансий
        :param vacacies_list:
        :return:
        """
        new_list = []

        for i in full_vacancies_list:
            record={}
            record["id"]=i["id"]
            print(i['id'])
            address = i["address"]
            print(address)
            addr1=json.dumps(address,ensure_ascii=False)
            print(addr1)
            addr2= json.loads(addr1)
            print(addr2)
            if address != None:
                record["city"] = addr2["city"]
                print(record['city'])
                record["street"] = addr2["street"]
                print(record['street'])
                if len(addr2["metro_stations"])>0:
                    record["metro"]=addr2["metro_stations"][0]["station_name"]
                else:
                    record["city"] = "NA"
                    record["metro"] = "NA"
                    record["street"] = "NA"

            else:
                record["city"] = "NA"
                record["metro"] = "NA"
                record["street"] = "NA"

            new_list.append(record)
        return new_list
