from fastapi import FastAPI

from app.crud import get_vacancies
from app.schemas import VacancyDB, AreaVacancy, SkillsDemand, SkillsSalary, PreviewInfo, ExperienceSalary
from app.services import (
    coloraise,
    get_skills_demand,
    get_skills_salary,
    preview_information,
    get_experience_salary,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/vacancies/", response_model=list[VacancyDB])
def get_all_vacancies(limit: int = 100, offset: int = 0):
    return get_vacancies(limit=limit, offset=offset)


@app.get("/api/areas/", response_model=list[AreaVacancy])
def get_areas():
    return coloraise()


@app.get("/api/charts/skills_demand/", response_model=list[SkillsDemand])
def get_skills_demand_chart_data(limit: int = 10):
    return get_skills_demand(limit)


@app.get("/api/charts/skills_salary/", response_model=SkillsSalary)
def get_skills_salary_chart_data(limit: int = 10):
    return get_skills_salary(limit)


@app.get("/api/charts/experience_salary", response_model=ExperienceSalary)
def get_experience_salary_chart_data():
    return get_experience_salary()


@app.get("/api/charts/preview_info", response_model=PreviewInfo)
def get_preview_info():
    return preview_information()
