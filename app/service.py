from fastapi import FastAPI
from app.crud import get_vacancies
from app.schemas import VacancyDB
from app.models import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/vacancies/", response_model=list[VacancyDB])
def get_all_vacansies(limit: int = 100):
    return get_vacancies(limit=limit)
