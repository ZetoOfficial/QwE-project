from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal
from app.models import Area as ORMArea
from app.models import Vacancy as ORMVacancy
from app.schemas import Area, AreaInput


class CRUDArea:
    @staticmethod
    async def create_area(input: AreaInput) -> Area:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                orm_obj = ORMArea(**input.__dict__)
                s.add(orm_obj)
            await s.commit()
        return orm_obj

    @staticmethod
    async def get_all_areas(limit: int = -1, offset: int = 0) -> list[Area]:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = select(ORMArea)
                if limit >= 0:
                    query = query.limit(limit)
                query = query.offset(offset)
                result = await s.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_areas_by_ids(ids: list[int]) -> list[Area]:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = select(ORMArea).where(ORMArea.id.in_(ids))
                result = await s.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_areas_by_code(code: str) -> list[Area]:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = select(ORMArea).where(ORMArea.code == code)
                result = await s.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_region_by_city(city: str) -> list[Area]:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = select(ORMArea).where(ORMArea.city == city)
                result = await s.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_area_instead_of_vacancies() -> list[tuple[str, str]]:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = (
                    select(ORMArea.code, ORMArea.region)
                    .where(ORMArea.city == ORMVacancy.area)
                    .order_by(ORMArea.code.desc())
                )
                result = await s.execute(query)
        return result.all()

    @staticmethod
    async def update_area(id: int, input: AreaInput) -> Area:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = update(ORMArea).where(ORMArea.id == id).values(**input.__dict__).returning(ORMArea)
                result = await s.execute(query)
            await s.commit()
        return result.one()

    @staticmethod
    async def delete_area(id: int) -> bool:
        async with SessionLocal() as s:
            s: AsyncSession
            async with s.begin():
                query = delete(ORMArea).where(ORMArea.id == id)
                await s.execute(query)
            await s.commit()
        return True
