from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from settings import settings as s

from app.crud import get_vacancies
from app.schemas import (
    AreaVacancy,
    ExperienceSalary,
    Filter,
    PreviewInfo,
    SkillsDemand,
    SkillsSalary,
    VacancyDB,
)
from app.services import (
    Downloader,
    coloraise,
    get_experience_salary,
    get_skills_demand,
    get_skills_salary,
    preview_information,
)

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


@app.get("/api/vacancies", response_model=list[VacancyDB])
def get_all_vacancies(limit: int = 100, offset: int = 0, filter_: Filter = None):
    return get_vacancies(limit=limit, offset=offset, filter_=filter_)


@app.get("/api/areas", response_model=list[AreaVacancy])
def get_areas():
    return coloraise()


@app.get("/api/charts/skills_demand", response_model=list[SkillsDemand])
def get_skills_demand_chart_data(limit: int = 10):
    return get_skills_demand(limit)


@app.get("/api/charts/skills_salary", response_model=SkillsSalary)
def get_skills_salary_chart_data(limit: int = 10):
    return get_skills_salary(limit)


@app.get("/api/charts/experience_salary", response_model=ExperienceSalary)
def get_experience_salary_chart_data():
    return get_experience_salary()


@app.get("/api/charts/preview_info", response_model=PreviewInfo)
def get_preview_info():
    return preview_information()


@app.get("/api/files/download_data")
def get_download_data(filename: str = "Вакансии", file_format: str = ".csv"):
    downloader = Downloader(s.app.media_folder)
    match file_format:
        case ".csv":
            path = downloader.download_as_csv()
        case ".xlsx":
            path = downloader.download_as_xlsx()
        case _:
            raise HTTPException(status_code=400, detail="Invalid file_format type")
    return FileResponse(path, media_type="application/octet-stream", filename=f"{filename}{file_format}")
