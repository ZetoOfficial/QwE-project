from fastapi import APIRouter

from app.schemas import ExperienceSalary, PreviewInfo, SkillsDemand, SkillsSalary
from app.services import ChartService

router = APIRouter()


@router.get("/skills_demand", response_model=list[SkillsDemand])
async def get_skills_demand(limit: int = 10):
    """Get data for a pie chart of the most demanded skills"""
    return await ChartService.get_skills_demand(limit)


@router.get("/skills_salary", response_model=SkillsSalary)
async def get_skills_salary(limit: int = 10):
    """Get data for a correlation diagram of wages and skills"""
    return await ChartService.get_skills_salary(limit)


@router.get("/experience_salary", response_model=ExperienceSalary)
async def get_experience_salary():
    """Get data for the correlation diagram of salary and work experience"""
    return await ChartService.get_experience_salary()


@router.get("/preview_info", response_model=PreviewInfo)
async def get_preview_info():
    """Get general information about vacancies"""
    return await ChartService.get_preview_info()
