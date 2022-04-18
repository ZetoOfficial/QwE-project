from requests import get as r_get
from json import loads
from app.schemas import Vacancies, Vacancy
from settings import settings as s


class HHParser:
    _api_url: str

    def __init__(self) -> None:
        self._api_url = s.app.hh_api_url

    def get_vacancy(self, id: int) -> Vacancy:
        """Получение подробной информации о вакансии по идентификатору

        Args:
            id (int): Идентификатор вакансии

        Returns:
            Vacancy: Вакансия
        """
        with r_get(f"{self._api_url}/vacancies/{id}") as req:
            return Vacancy.parse_obj(loads(req.content.decode()))

    def get_initial_data(self, search_text: str = "NAME:Backend", area: int = 113) -> Vacancies:
        """Получение общей иниформации о кол-ве вакансий

        Args:
            search_text (_type_, optional): Название вакансий. Defaults to "NAME:Backend".
            area (int, optional): Регион поиска. Defaults to 113 (Россия).

        Returns:
            Vacancies: Общая информация о вакансиях
        """
        params = {
            "text": search_text,
            "area": area,
            "page": 0,
            "per_page": 100,
        }
        with r_get(f"https://api.hh.ru/vacancies", params) as req:
            return Vacancies.parse_obj(loads(req.content.decode()))

    def getPage(self, page: int = 0, search_text: str = "NAME:Backend", area: int = 113) -> list[Vacancy]:
        """Получение подробных вакансий со страницы

        Args:
            page (int, optional): Страница в поиске. Defaults to 0.
            search_text (_type_, optional): Название вакансии. Defaults to "NAME:Backend".
            area (int, optional): Регион поиска. Defaults to 113 (Россия).

        Returns:
            list[Vacancy]: Список вакансий с подробной информацией
        """

        params = {
            "text": search_text,
            "area": area,
            "page": page,
            "per_page": 100,
        }
        with r_get("https://api.hh.ru/vacancies", params) as req:
            data = loads(req.content.decode()).get("items", [])
        return [self.get_vacancy(item.get("id")) for item in data]
