import json
import os
from abc import ABC, abstractmethod
from pprint import pprint

import requests


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """
        Возвращает экземпляр
        класса Connector
        """
        pass


class HH(Engine):
    URL = 'https://api.hh.ru/vacancies/'

    def __init__(self, search_keyword):
        super().__init__()
        self.search_keyword = search_keyword
        self.params = {
            'text': f'{self.search_keyword}',
            'per_page': 100,
            'area': 113,
            'page': 0
            }

    def get_request(self):
        response = requests.get(self.URL, params=self.params)
        data = response.content.decode()
        response.close()
        json_hh = json.loads(data)
        return json_hh

    def info_vacancies(self, info):
        data = {
                'from': 'HeadHunter',
                'name': info.get('name'),
                'url': info.get('alternate_url'),
                'description': info.get('snippet').get('responsibility'),
                'salary': info.get('salary'),
                'date_published': info.get('published_at'),
                'experience': info.get('experience'),
                'page_number': info.get('page')
                }

        return data

    @property
    def get_vacancies(self):
        vacancies_hh = []
        while len(vacancies_hh) <= 500:
            data = self.get_request()
            items = data.get('items')
            if not items:
                break
            for vacancy_hh in items:
                if vacancy_hh.get('salary') is not None and vacancy_hh.get('salary').get('currency') == 'RUR':
                    vacancies_hh.append(self.info_vacancies(vacancy_hh))

            self.params['page'] += 1

        return vacancies_hh

    def to_json(self, data):
        with open("filename.json", "w", encoding="UTF-8") as name_file:
            json.dump(data, name_file, indent=2, ensure_ascii=False)


class Superjob(Engine):
    URL = 'https://api.superjob.ru/2.0/vacancies/'

    def __init__(self, search_keyword):
        super().__init__()
        self.search_keyword = search_keyword
        self.params = {'keywords': f'{search_keyword}', 'count': 100, 'page': 0}

    def get_request(self):
        api_key: str = os.getenv('api_key')
        HEADERS = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': api_key,
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.get(self.URL, headers=HEADERS, params=self.params)
        data = response.content.decode()
        response.close()

        js_superjob = json.loads(data)
        return js_superjob

    def info_vacancies(self, info):
        data = {
                'from': 'Superjob',
                'name': info.get('profession'),
                'url': info['link'],
                'description': info.get('client').get('description'),
                'salary': info['currency'],
                'date_published': info['date_published']
                }

        return data

    @property
    def get_vacancies(self):
        vacancies_sj = []
        while len(vacancies_sj) <= 500:
            data = self.get_request()
            items = data.get('objects')
            if not items:
                break
            for vacancy_sj in items:
                if vacancy_sj.get('currency') is not None and vacancy_sj.get('currency') == 'rub':
                    vacancies_sj.append(self.info_vacancies(vacancy_sj))

            self.params['page'] += 1

        return vacancies_sj

    def to_json(self, data):
        with open("filename.json", "w", encoding="UTF-8") as name_file:
            json.dump(data, name_file, indent=2, ensure_ascii=False)


class Vacancy:
    def __init__(self, name_vacancy, url_vacancy, description, salary):
        self.name_vacancy = name_vacancy
        self.url_vacancy = url_vacancy
        self.description = description
        self.salary = salary

    def __repr__(self):
        return f'Вакансия {self.name_vacancy} - зарплата {self.salary}'


if __name__ == '__main__':
    hh = HH('Python')
    info = hh.get_request()
    print(len(info))
    #pprint(info)
    #vacancy = hh.get_vacancies
    #print(len(vacancy))
    #hh.to_json(vacancy)
    #print(f"\n")
    sj = Superjob('Python')
    #pprint(sj.get_request())
    vacancy = sj.get_vacancies
    sj.to_json(vacancy)
    print(len(vacancy))
