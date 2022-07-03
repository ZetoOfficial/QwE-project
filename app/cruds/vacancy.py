from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.models import Vacancy as ORMVacancy
from app.schemas import Vacancy, VacancyInput


class CRUDVacancy:
    @staticmethod
    async def create_vacancy(input: VacancyInput) -> Vacancy:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                orm_obj = ORMVacancy(**input.__dict__)
                s.add(orm_obj)
            await s.commit()
        return orm_obj

    @staticmethod
    async def get_all_vacancies(limit: int = -1, offset: int = 0) -> list[Vacancy]:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = select(ORMVacancy)
                if limit >= 0:
                    query = query.limit(limit)
                query = query.offset(offset)
                result = await s.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_vacancies_by_ids(ids: list[int]) -> list[Vacancy]:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = select(ORMVacancy).where(ORMVacancy.id.in_(ids))
                result = await s.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_vacancy(id: int, input: VacancyInput) -> Vacancy:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = (
                    update(ORMVacancy)
                    .where(ORMVacancy.id == id)
                    .values(**input.__dict__)
                    .returning(ORMVacancy)
                )
                result = await s.execute(query)
            await s.commit()
        return result.one()

    @staticmethod
    async def delete_vacancy(id: int) -> bool:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = delete(ORMVacancy).where(ORMVacancy.id == id)
                await s.execute(query)
            await s.commit()
        return True
