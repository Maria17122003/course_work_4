import json
from classes import *


def get_top_vacancies(name_file, count):
    """
    Возвращает самые
    высокооплачиваемые вакансии
    """
    with open(name_file, encoding="UTF-8") as file:
        list_vacancies_hh = json.load(file)
        vacancies = []
        for item in list_vacancies_hh:
            if item["payment_from"] is None:
                item["payment_from"] = item["payment_to"]
            vacancies.append(item)
        sorted_vacancies_hh = sorted(vacancies, key=lambda i: i['payment_from'], reverse=True)
        top_vacancies = sorted_vacancies_hh[:count]
        return top_vacancies


def get_formatted_vacancies(vacancies):
    """
    Форматирует вакансии в нужный формат
    """
    formatted_vacancies = []

    for i in vacancies:
        name = i['name']
        description = i["description"]
        salary = i["payment_from"]
        url = i['url']

        formatted_vacancies.append(f"""\
    {name} - {description}
    зарплата - {salary} 
    {url}\n""")

    return formatted_vacancies


def user_interaction(platforms_input, search_query, top_n):
    """
    Выводит пользователю
    вакансии
    """
    platforms = ["HeadHunter", "SuperJob"]
    if platforms_input == platforms[0]:
        hh = HH(search_query)
        data = hh.get_vacancies_hh
        hh.to_json(data)
        top_vacancies = get_top_vacancies('vacancies_hh.json', top_n)
        return get_formatted_vacancies(top_vacancies)
    if platforms_input == "SuperJob":
        sj = Superjob(search_query)
        data = sj.get_vacancies_sj
        sj.to_json(data)
        top_vacancies = get_top_vacancies('vacancies_superjob.json', top_n)
        return get_formatted_vacancies(top_vacancies)
    else:
        return None
