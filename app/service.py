from fastapi import FastAPI

from app.crud import get_vacancies
from app.schemas import VacancyDB, AreaVacancy
from app.services.map import coloraise
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
def get_all_vacancies(limit: int = 100):
    return get_vacancies(limit=limit)


@app.get("/api/areas/", response_model=list[AreaVacancy])
def get_areas():
    return coloraise()
