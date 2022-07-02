from fastapi import APIRouter

from app.schemas import Area, AreaColor
from app.services import AreaService

router = APIRouter()


@router.get("/areas", response_model=list[Area])
async def get_areas(limit: int = 100, offset: int = 0):
    """Get all areas from database"""
    return await AreaService.get_all_areas(limit, offset)


@router.get("/color_regions", response_model=list[AreaColor])
async def get_area_colors_for_vacancies():
    """Get the regions with the number of vacancies and color"""
    return await AreaService.get_areas_with_vacancy_count()
