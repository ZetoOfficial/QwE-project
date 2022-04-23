from json import loads

from requests import get as r_get

from app.schemas import Vacancies, Vacancy
from app.crud import create_vacancy, get_vacancy_by_id
from settings import settings as s, getLogger

logger = getLogger(__name__)


class HHParser:
    _api_url: str = s.app.hh_api_url
    _per_page: int = 100

    def get_vacancy(self, id: int) -> Vacancy:
        """Получение подробной информации о вакансии по идентификатору

        Args:
            id (int): Идентификатор вакансии

        Returns:
            Vacancy: Вакансия
        """
        logger.debug(f"Получение вакансии: {id}")
        if vacancy := get_vacancy_by_id(id):
            logger.debug(f"Вакансия получена: {vacancy.name}")
            return vacancy
        with r_get(f"{self._api_url}/vacancies/{id}") as req:
            vacancy = create_vacancy(Vacancy.parse_obj(loads(req.content.decode())))
            logger.debug(f"Вакансия получена: {vacancy.name}")
            return vacancy

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
            "per_page": self._per_page,
        }
        logger.debug("Инициализация запроса")
        with r_get(f"{self._api_url}/vacancies", params) as req:
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
            "per_page": self._per_page,
        }
        with r_get(f"{self._api_url}/vacancies", params) as req:
            data = loads(req.content.decode()).get("items", [])
            logger.info(f"Получено {len(data)} вакансий с {page} стр")

        return [self.get_vacancy(item.get("id")) for item in data]
