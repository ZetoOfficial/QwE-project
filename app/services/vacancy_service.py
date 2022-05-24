from typing import Optional

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import SessionLocal
from app.models import Vacancy
from app.models.models_dto import CreateVacancyDTO, UpdateVacancyDTO


class IVacancyService:
    @staticmethod
    async def get_all_vacancies(limit: int):
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = select(Vacancy).limit(limit)
                result = await s.execute(query)
        return result

    @staticmethod
    async def get_vacancy_by_ids(ids: list[int]) -> Optional[list[Vacancy]]:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = select(Vacancy).where(Vacancy.id.in_(ids))
                result = await s.execute(query)
        return result

    @staticmethod
    async def create_vacancy(dto: CreateVacancyDTO) -> Vacancy:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                orm_obj = Vacancy(dto)
                s.add(orm_obj)
            await s.commit()
        return orm_obj

    @staticmethod
    async def update_vacancy(dto: UpdateVacancyDTO, vacancy_id: int) -> Vacancy:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                orm_obj = update(Vacancy).where(Vacancy.id == vacancy_id).values(dto).returning(Vacancy)
                result = await s.execute(orm_obj)
            await s.commit()
        return result.mappings().one()

    @staticmethod
    async def delete_vacancy(vacancy_id: int):
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                orm_obj = delete(Vacancy).where(Vacancy.id == vacancy_id)
                await s.execute(orm_obj)
            await s.commit()
        return True
