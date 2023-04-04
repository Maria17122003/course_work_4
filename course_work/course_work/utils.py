import json

from classes import *


def get_top_vacancies(name_file, count):
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
    Форматирует операции в нужный формат
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
    platforms = ["HeadHunter", "SuperJob"]
    if platforms_input == platforms[0]:
        hh = HH(search_query)
        data = hh.get_vacancies_hh
        hh.to_json(data)
        top_vacancies = get_top_vacancies('vacancies_hh.json', top_n)
        return get_formatted_vacancies(top_vacancies)
    elif platforms_input == platforms[1]:
        sj = Superjob(search_query)
        data = sj.get_vacancies_sj
        sj.to_json(data)
        top_vacancies = get_top_vacancies('vacancies_superjob.json', top_n)
        return get_formatted_vacancies(top_vacancies)
    else:
        return "Данная платформа не представлена"

    #filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)


if __name__ == '__main__':
    hh = HH('Python')
    info = hh.get_request()
    #pprint(info)
    vacancy = hh.get_vacancies_hh
    #print(len(vacancy))
    hh.to_json(vacancy)
    #print(len(get_top_vacancies('vacancies_hh.json', 10)))
    #pprint(get_top_vacancies('vacancies_hh.json', 10))
    platforms_input = input("Введите платформу, с которой хотите получить вакансии: ")
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    user = user_interaction(platforms_input, search_query, top_n)
    for item in user:
        print(item)
    #print(f"\n")
    sj = Superjob('Python')
    #pprint(sj.get_request())
    vacancy = sj.get_vacancies_sj
    sj.to_json(vacancy)
    #print(len(vacancy))
