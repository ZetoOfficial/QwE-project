from fastapi import APIRouter

from app.schemas import Vacancy
from app.services import VacancyService

router = APIRouter()


@router.get("/vacancies", response_model=list[Vacancy])
async def get_all_vacancies(limit: int = 100, offset: int = 0):
    """Get all vacancies from the database"""
    return await VacancyService.get_all_vacancies(limit, offset)
