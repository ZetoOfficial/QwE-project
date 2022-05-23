from collections import Counter

from app.crud import get_all_areas, get_vacancies_for_areas
from app.schemas import AreaVacancy


def get_color(count: int) -> str:
    """Получение цвета на основе числа"""
    match count:
        case c if c in range(3):
            return "#D3D3D3"
        case c if c in range(6):
            return "#BEBEBE"
        case c if c in range(11):
            return "#A0A0A0"
        case c if c in range(20):
            return "#888888"
        case c if c in range(30):
            return "#686868"
        case c if c in range(50):
            return "#585858"
        case c if c in range(75):
            return "#484848"
        case _:
            return "#202020"


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
