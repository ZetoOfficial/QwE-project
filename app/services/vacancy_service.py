from collections import Counter, defaultdict

from app.cruds import CRUDVacancy
from app.database import SessionLocal
from app.models import Vacancy as ORMVacancy
from app.schemas import Vacancy, VacancyInput


class VacancyService:
    @staticmethod
    async def create_vacancy(input: VacancyInput) -> Vacancy:
        return await CRUDVacancy.create_vacancy(input)

    @staticmethod
    async def get_all_vacancies(limit: int, offset: int) -> list[Vacancy]:
        return await CRUDVacancy.get_all_vacancies(limit, offset)

    @staticmethod
    async def get_vacancies_by_ids(ids: list[int]) -> list[Vacancy]:
        return await CRUDVacancy.get_vacancies_by_ids(ids)

    @staticmethod
    async def get_skills_demand():
        vacancies = await CRUDVacancy.get_all_vacancies(0, 0)
        vacancies = list(filter(lambda v: v.key_skills and v.salary, vacancies))
        skills = defaultdict(int)

        # for vacancy in vacancies:
        #     for skill in vacancy.key_skills:
        #         skills[skill] += 1

        # return skills
