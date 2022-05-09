from json import loads

from requests import get as r_get

from app.schemas import Vacancies, Vacancy, Area
from app.crud import create_vacancy, get_vacancy_by_id, create_area, update_vacancy
from settings import settings as s, getLogger

from .regions_parser import RegionParser

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
        with r_get(f"{self._api_url}/vacancies/{id}") as req:
            if not (vacancy := get_vacancy_by_id(id)):
                vacancy = Vacancy.parse_obj(loads(req.content.decode()))
            logger.debug(f"Вакансия получена: {vacancy.name}")
            # vacancy.description = "???"
            # update_vacancy(vacancy)
            return create_vacancy(vacancy)

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

    def get_areas(self):
        with r_get(f"{self._api_url}/areas/113/") as req:
            data = loads(req.content.decode()).get("areas", [])
        reg_parser = RegionParser()
        city_codes = reg_parser.get_city_codes()
        for region in data:
            rs1 = region["name"].replace("АО", "автономный округ").lower()
            rs2 = region["name"].replace("АО", "автономная область").lower()
            code_ = None
            if int(region["id"]) == 1368:  # Ханты-Мансийский АО - Югра"
                code_ = "86"
            elif int(region["id"]) == 1475:  # Республика Северная Осетия-Алания
                code_ = "15"
            if not len(region["areas"]):
                create_area(
                    Area(
                        id=int(region["id"]),
                        city=region["name"],
                        code=city_codes.get(rs1) or city_codes.get(rs2) or code_,
                        region=region["name"],
                    )
                )
                logger.info(f'{int(region["id"])} {region["name"]} {region["name"]}')
            for city in region["areas"]:
                create_area(
                    Area(
                        id=int(city["id"]),
                        city=city["name"],
                        code=city_codes.get(rs1)
                        or city_codes.get(rs2)
                        or city_codes.get(city["name"])
                        or code_,
                        region=region["name"],
                    )
                )
                logger.info(f'{int(city["id"])} {city["name"]} {region["name"]}')
