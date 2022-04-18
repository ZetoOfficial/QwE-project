from fastapi import FastAPI
from app.crud import get_vacancy_by_id, get_vacancies
from app.schemas import Vacancy

app = FastAPI()


@app.get("/vacancies/", response_model=list[Vacancy])
def get_all_vacansies():
    return get_vacancies()


@app.get("/vacancies/{vacancy__id}", response_model=Vacancy)
def get_vacancy(vacancy_id: int = 0):
    return get_vacancy_by_id(vacancy_id=vacancy_id)
