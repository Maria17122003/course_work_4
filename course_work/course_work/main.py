from course_work.course_work.utils import *

if __name__ == '__main__':
    print("Вас приветстувует программа по подбору вакансий")
    platforms_input = input("Введите платформу, с которой хотите получить вакансии: ")
    search_query = input("Введите ключевое слово поиска: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    user = user_interaction(platforms_input, search_query, top_n)
    if user is not None:
        for item in user:
            print(item)
        print(f"Вы можете добавить или удалить понравившуюся вакансию\nУкажите 'Добавить', 'Удалить', 'Закончить'")
        option = input()
        json_saver = JSONSaver()
        while option != "Закончить":
            if option == 'Добавить':
                like_vacancy = input("Укажите ссылку ")
                json_saver.like_vacancy(platforms_input, like_vacancy)
                print(f"Вакансия добавлена\nУкажите 'Добавить', 'Удалить', 'Закончить'")
                option = input()
            elif option == 'Удалить':
                del_vacancy = input("Укажите ссылку ")
                json_saver.delete_vacancy(del_vacancy)
                print(f"Вакансия удалена\nУкажите 'Добавить', 'Удалить', 'Закончить'")
                option = input()
            else:
                option = input("Нет такой команды, повторите попытку ")

        json_saver.list_vacancy()
        print("Вакансии по вашему запросу показаны, понравившиеся добавлены")
    else:
        print("Данная платформа не представлена")
