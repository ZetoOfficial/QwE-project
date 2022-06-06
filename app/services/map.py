from collections import Counter

from app.crud import get_all_areas, get_vacancies_for_areas
from app.schemas import AreaVacancy


def get_color(count: int) -> str:
    """Получение цвета на основе числа"""
    match count:
        case c if c in range(3):
            return "#d5d8f2"
        case c if c in range(6):
            return "#959bd0"
        case c if c in range(11):
            return "#aaaed3"
        case c if c in range(20):
            return "#979ac6"
        case c if c in range(30):
            return "#6f739a"
        case c if c in range(50):
            return "#4c5285"
        case c if c in range(75):
            return "#393f7a"
        case _:
            return "#2c326a"


def coloraise() -> list[AreaVacancy]:
    """Соотносит кол-во вакансий в регионе с цветом"""
    areas = get_all_areas()
    vacancies = get_vacancies_for_areas()
    all_vacancies_area = Counter([vac for vac in vacancies]).items()

    out = list()
    for area in areas:
        data = {"city": {"code": area.code, "region": area.region}, "cnt": 0, "color": get_color(0)}
        if data not in out:
            out.append(data)
    for item in all_vacancies_area:
        data = {"city": {"code": item[0][0], "region": item[0][1]}, "cnt": 0, "color": get_color(0)}
        index = out.index(data)
        out[index] = {"city": item[0], "cnt": item[1], "color": get_color(item[1])}
    return sorted(out, key=lambda i: i["cnt"], reverse=True)
