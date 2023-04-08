import json
import os
from abc import ABC, abstractmethod
import requests


class Engine(ABC):
    """
    Абстрактный класс
    """
    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    """
    Класс платформы
    HH
    """
    URL = 'https://api.hh.ru/vacancies/'

    def __init__(self, search_keyword):
        """
        Инициализирует слово,
        по которому происходит поиск вакансий
        """
        super().__init__()
        self.search_keyword = search_keyword
        self.params = {
            'text': f'{self.search_keyword}',
            'per_page': 100,
            'area': 113,
            'page': 0
            }

    def get_request(self):
        """
        Получает вакансии по API
        """
        response = requests.get(self.URL, params=self.params)
        data = response.content.decode()
        response.close()
        json_hh = json.loads(data)
        return json_hh

    def info_vacancies_hh(self, vacancies):
        """
        Структурирует получаемые
        из API данные по ключам
        """
        data = {
                'from': 'HeadHunter',
                'name': vacancies.get('name'),
                'url': vacancies.get('alternate_url'),
                'description': vacancies.get('snippet').get('responsibility'),
                'payment_from': vacancies['salary']['from'],
                'payment_to': vacancies['salary']['to'],
                'salary': vacancies['salary']['currency'],
                'date_published': vacancies.get('published_at'),
                'experience': vacancies.get('experience'),
                'page_number': vacancies.get('page')
                }

        return data

    @property
    def get_vacancies_hh(self):
        """
        Получает вакансии
        при наличии информации
        о ЗП
        """
        vacancies_hh = []
        while len(vacancies_hh) <= 1000:
            data = self.get_request()
            items = data.get('items')
            if not items:
                break
            for vacancy_hh in items:
                if vacancy_hh.get('salary') is not None and vacancy_hh.get('salary').get('currency') == 'RUR':
                    vacancies_hh.append(self.info_vacancies_hh(vacancy_hh))

            self.params['page'] += 1

        return vacancies_hh

    def to_json(self, data):
        """
        Создает файл,
        добавляет в него
        вакансии
        """
        with open("vacancies_hh.json", "w", encoding="UTF-8") as name_file:
            json.dump(data, name_file, indent=2, ensure_ascii=False)


class Superjob(Engine):
    """
    Класс платформы
    Superjob
    """
    URL = 'https://api.superjob.ru/2.0/vacancies/'

    def __init__(self, search_keyword):
        """
        Инициализирует слово,
        по которому происходит поиск вакансий
        """
        super().__init__()
        self.search_keyword = search_keyword
        self.params = {
            'keywords': f'{search_keyword}',
            'count': 100,
            'area': 113,
            'page': 0
        }

    def get_request(self):
        """
        Получает вакансии по API
        """
        api_key: str = os.getenv('api_key')
        headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': api_key,
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.get(self.URL, headers=headers, params=self.params)
        data = response.content.decode()
        response.close()

        sj_superjob = json.loads(data)
        return sj_superjob

    def info_vacancies_sj(self, vacancies):
        """
        Структурирует получаемые
        из API данные по ключам
        """
        data = {
                'from': 'Superjob',
                'name': vacancies.get('profession'),
                'url': vacancies['link'],
                'description': vacancies.get('client').get('description'),
                'payment_from': vacancies['payment_from'],
                'payment_to': vacancies['payment_to'],
                'salary': vacancies['currency'],
                'date_published': vacancies['date_published']
                }

        return data

    @property
    def get_vacancies_sj(self):
        """
        Получает вакансии
        при наличии информации
        о ЗП
        """
        vacancies_sj = []
        while len(vacancies_sj) <= 1000:
            data = self.get_request()
            items = data.get('objects')
            if not items:
                break
            for vacancy_sj in items:
                if vacancy_sj['payment_from'] is not None and vacancy_sj.get('currency') == 'rub':
                    vacancies_sj.append(self.info_vacancies_sj(vacancy_sj))

            self.params['page'] += 1

        return vacancies_sj

    def to_json(self, data):
        """
        Создает файл,
        добавляет в него
        вакансии
        """
        with open("vacancies_superjob.json", "w", encoding="UTF-8") as name_file:
            json.dump(data, name_file, indent=2, ensure_ascii=False)


class Vacancy:
    """
    Класс для вакансий
    """
    def __init__(self, name_vacancy, url_vacancy, description, salary):
        """
        Инициализирует
        название вакансии, ссылку,
        описание и зарплату
        """
        self.name_vacancy = name_vacancy
        self.url_vacancy = url_vacancy
        self.description = description
        self.salary = salary

    def __repr__(self):
        return f'Вакансия {self.name_vacancy} - зарплата {self.salary}'

    def __lt__(self, other):
        """
        Сравнивает зарплату
        """
        if int(self.salary) < int(other.salary):
            return True
        return False

    def __gt__(self, other):
        """
        Сравнивает зарплату
        """
        if int(self.salary) > int(other.salary):
            return True
        return False

    def get_list_vacancies(self):
        """
        Структурирует данные
        о вакансиях
        по ключам
        """
        data = {
            'name': self.name_vacancy,
            'url': self.url_vacancy,
            'description': self.description,
            'salary': self.salary,
        }

        return data


class JSONSaver:
    """
    Класс для сохранения
    понравившихся вакансий
    """
    def __init__(self):
        self.vacancies = []

    def like_vacancy(self, platform, url):
        """
        Добавляет в список
        понравившиеся вакансии
        """
        cache = []
        if platform == "HeadHunter":
            with open('vacancies_hh.json', 'r', encoding='utf-8') as name_file:
                data = json.load(name_file)
            for item in data:
                if url == item['url']:
                    cache.append(item)
                    for i in cache:
                        if i not in self.vacancies:
                            self.vacancies.append(item)

        else:
            with open('vacancies_superjob.json', 'r', encoding='utf-8') as name_file:
                data = json.load(name_file)
            for item in data:
                if url == item['url']:
                    cache.append(item)
                    for i in cache:
                        if i not in self.vacancies:
                            self.vacancies.append(item)

        return self.vacancies

    def delete_vacancy(self, del_url_vacancy):
        """
        Удаляет из списка
        вакансии
        """
        count = 0
        for txt in self.vacancies:
            if txt['url'] == del_url_vacancy:
                self.vacancies.pop(count)
            else:
                count += 1

        return self.vacancies

    def list_vacancy(self):
        """
        Сохраняет список
        в файл
        """
        with open("vacancies_like.json", "w", encoding="UTF-8") as name_file:
            json.dump(self.vacancies, name_file, indent=2, ensure_ascii=False)
