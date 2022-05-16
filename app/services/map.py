from collections import Counter

from app.crud import get_vacancies_for_areas
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
    all_areas = Counter([vac for vac in get_vacancies_for_areas()]).items()
    out = []
    for item in sorted(all_areas, key=lambda i: i[1], reverse=True):
        out.append(AreaVacancy.parse_obj({"city": item[0], "cnt": item[1], "color": get_color(item[1])}))
    return out
