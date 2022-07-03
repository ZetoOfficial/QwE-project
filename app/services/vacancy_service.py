from collections import Counter, defaultdict

from app.cruds import CRUDVacancy
from app.schemas import Vacancy, VacancyInput


class VacancyService:
    @staticmethod
    async def create_vacancy(input: VacancyInput) -> Vacancy:
        return await CRUDVacancy.create_vacancy(input)

    @staticmethod
    async def get_all_vacancies(limit: int = -1, offset: int = -1) -> list[Vacancy]:
        return await CRUDVacancy.get_all_vacancies(limit, offset)

    @staticmethod
    async def get_vacancies_by_ids(ids: list[int]) -> list[Vacancy]:
        return await CRUDVacancy.get_vacancies_by_ids(ids)
