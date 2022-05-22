import json
from typing import Optional

import requests

from app.crud import create_area, create_vacancy, get_vacancy_by_id, update_vacancy
from app.schemas import Area, Salary, Vacancy
from settings import getLogger

from .regions_parser import RegionParser

logger = getLogger(__name__)


class HHParser:
    _api_url: str
    _per_page: int
    _dictionaries: dict

    def __init__(self, url: str, per_page: int):
        self._api_url = url
        self._per_page = per_page
        self._dictionaries = self.get_dictionaries()

    def get_dictionaries(self) -> dict:
        return requests.get(f"{self._api_url}/dictionaries").json()

    def get_currency_info(self, code: str) -> dict:
        return next(
            curr for curr in self._dictionaries["currency"] if curr["code"] == code
        )

    def convert_salary(self, salary: Salary) -> Optional[int]:
        if salary is None or salary.start is None and salary.to is None:
            return None
        if salary.start and salary.to:
            total = (salary.start + salary.to) // 2
        else:
            total = (salary.start or 0) + (salary.to or 0)
        currency = self.get_currency_info(salary.currency)
        return int(total / currency["rate"])

    def get_vacancy(self, id: int) -> Vacancy:
        """Получение подробной информации о вакансии по идентификатору

        Args:
            id (int): Идентификатор вакансии

        Returns:
            Vacancy: Вакансия
        """
        logger.debug(f"Получение вакансии: {id}")
        if vacancy := get_vacancy_by_id(id):
            return vacancy
        with requests.get(f"{self._api_url}/vacancies/{id}") as req:
            vacancy = Vacancy.parse_obj(json.loads(req.content.decode()))
            if vacancy.salary:
                vacancy.salary.total = self.convert_salary(vacancy.salary)
            logger.debug(f"Получена новая вакансия: {vacancy.name}")
            return create_vacancy(vacancy)

    def get_page(self, params: dict = {}) -> list[Vacancy]:
        """Получение подробных вакансий со страницы

        Args:
            params (dict, optional): Дополнительные параметры для запроса. По умолчанию их нет.

        Returns:
            list[Vacancy]: Список вакансий с подробной информацией
        """
        with requests.get(f"{self._api_url}/vacancies", params) as req:
            data = json.loads(req.content.decode())
            logger.info(
                f"Получено {len(data.get('items', []))} вакансий с {data.get('page', 0)} стр"
            )

        return [self.get_vacancy(item.get("id")) for item in data.get("items", [])]

    def get_all_vacancies_data(
        self, search_text: str = "NAME:Backend", area: int = 113
    ) -> list[Vacancy]:
        """Получение всех вакансий (с подробностями)

        Args:
            search_text (_type_, optional): Название вакансий. По умолчанию "NAME:Backend".
            area (int, optional): Регион поиска. По умолчанию 113 (Россия).

        Returns:
            Vacancies: Общая информация о вакансиях
        """
        params = {
            "text": search_text,
            "area": area,
            "page": 0,
            "per_page": self._per_page,
        }
        logger.info("Инициализация запроса")
        with requests.get(f"{self._api_url}/vacancies", params) as req:
            first_page = json.loads(req.content.decode())
        all_pages = []
        for page in range(0, first_page.get("pages", 1)):
            params["page"] = page
            all_pages += self.get_page(params)
            logger.info(f"Собрано {len(all_pages)} из {first_page['found']}")
        return all_pages

    def save_and_get_areas(self, parent_area: int = 113) -> list[Area]:
        """Сохранение (в бд) и получение Areas (код, регион, город)

        Args:
            parent_area (int, optional): Регион поиска. По умолчанию 113 (Россия). Другие пока не поддерживаются...

        Returns:
            list[Area]: Список полученных Areas (код, регион, город)
        """
        with requests.get(f"{self._api_url}/areas/{parent_area}/") as req:
            data = json.loads(req.content.decode()).get("areas", [])
        reg_parser = RegionParser()
        city_codes = reg_parser.get_city_codes()
        output_areas = []
        for region in data:
            rs1 = region["name"].replace("АО", "автономный округ").lower()
            rs2 = region["name"].replace("АО", "автономная область").lower()
            code_ = None
            if int(region["id"]) == 1368:  # Ханты-Мансийский АО - Югра"
                code_ = "86"
            elif int(region["id"]) == 1475:  # Республика Северная Осетия-Алания
                code_ = "15"
            if not len(
                region["areas"]
            ):  # На случай, если у региона нет городов (Москва, например)
                region["areas"].append({"id": region["id"], "name": region["name"]})
            for city in region["areas"]:
                output_areas.append(
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
                )
                logger.info(f'{int(city["id"])} {city["name"]} {region["name"]}')
        return output_areas
