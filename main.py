from requests import get as r_get
from json import loads
from time import sleep
from csv import DictWriter
from app.schemas import Vacancies, Vacancy


def get_vacancy(id: int) -> Vacancy:
    """_summary_

    Args:
        id (int): _description_

    Returns:
        Vacancy: _description_
    """
    sleep(0.25)
    with r_get(f"https://api.hh.ru/vacancies/{id}") as req:
        data = loads(req.content.decode())
        return Vacancy.parse_obj(data)


def get_initial_data() -> Vacancies:
    params = {
        "text": "NAME:Backend",  # NAME:Backend Текст фильтра. В имени должно быть слово "Backend"
        "area": 113,  # Поиск ощуществляется по вакансиям России
        "page": 0,  # Индекс страницы поиска на HH
        "per_page": 100,  # Кол-во вакансий на 1 странице
    }
    with r_get(f"https://api.hh.ru/vacancies", params) as req:
        return Vacancies.parse_obj(loads(req.content.decode()))


def getPage(page: int = 0) -> list[Vacancy]:
    """
    Создаем метод для получения страницы со списком вакансий.

    Args:
        page (int, optional): Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница

    Returns:
        str: вакансии
    """
    params = {
        "text": "NAME:Backend",  # NAME:Backend Текст фильтра. В имени должно быть слово "Backend"
        "area": 113,  # Поиск ощуществляется по вакансиям России
        "page": page,  # Индекс страницы поиска на HH
        "per_page": 100,  # Кол-во вакансий на 1 странице
    }
    with r_get("https://api.hh.ru/vacancies", params) as req:  # Посылаем запрос к API
        data = loads(req.content.decode()).get("items", [])
    return [get_vacancy(item.get("id")) for item in data]


all_vacancies = []
first_page = get_initial_data()
pages = first_page.pages
for page in range(1, pages):
    all_vacancies += getPage(page)
    print(f"Вакансии: {page}/{pages} ({len(all_vacancies)})")
    sleep(0.25)


with open("vacancies.csv", "w", newline="") as output_file:
    dict_writer = DictWriter(output_file, dict(all_vacancies[0]).keys())
    dict_writer.writeheader()
    dict_writer.writerows(all_vacancies)
