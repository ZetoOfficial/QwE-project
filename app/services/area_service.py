from collections import Counter
from typing import Dict

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import CRUDArea, CRUDVacancy
from app.database import SessionLocal
from app.models import Area as ORMArea
from app.schemas import Area, AreaInput
from app.utils import int_to_color


class AreaService:
    @staticmethod
    async def create_area(input: AreaInput) -> Area:
        return await CRUDArea.create_area(input)

    @staticmethod
    async def get_all_areas(limit: int, offset: int) -> list[Area]:
        return await CRUDArea.get_all_areas(limit, offset)

    @staticmethod
    async def get_areas_by_ids(ids: list[int]) -> list[Area]:
        return await CRUDArea.get_areas_by_ids(ids)

    @staticmethod
    async def get_areas_by_code(code: str) -> list[Area]:
        return await CRUDArea.get_areas_by_code(code)

    @staticmethod
    async def get_region_by_city(city: str) -> list[Area]:
        return await CRUDArea.get_region_by_city(city)

    @staticmethod
    async def get_areas_with_vacancy_count() -> list[Dict]:
        areas = await CRUDArea.get_all_areas(0, 0)
        instead_areas = await CRUDArea.get_area_instead_of_vacancies()
        default_color = int_to_color(0)
        all_vacancies_area = Counter(instead_areas).items()

        out = list()
        for area in areas:
            data = {"city": {"code": area.code, "region": area.region}, "cnt": 0, "color": default_color}
            if data not in out:
                out.append(data)

        for item in all_vacancies_area:
            data = {"city": {"code": item[0][0], "region": item[0][1]}, "cnt": 0, "color": default_color}
            index = out.index(data)
            out[index] = {"city": item[0], "cnt": item[1], "color": int_to_color(item[1])}
        return out

    @staticmethod
    async def update_area(id: int, input: AreaInput) -> Area:
        return await CRUDArea.update_area(id, input)

    @staticmethod
    async def delete_area(id: int) -> bool:
        return await CRUDArea.delete_area(id)
