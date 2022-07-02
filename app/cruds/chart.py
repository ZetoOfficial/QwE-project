from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.models import Vacancy as ORMVacancy


class CRUDChart:
    @staticmethod
    async def get_all_skills():
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = (
                    select(ORMVacancy.key_skills, ORMVacancy.salary)
                    .where(ORMVacancy.key_skills.is_not(None), ORMVacancy.salary.is_not(None))
                    .order_by(ORMVacancy.salary)
                )
                result = await s.execute(query)
        return result.all()

    @staticmethod
    async def get_experience_and_salary():
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = select(ORMVacancy.experience, ORMVacancy.salary).where(
                    ORMVacancy.salary.is_not(None)
                )
                result = await s.execute(query)
        return result.all()
