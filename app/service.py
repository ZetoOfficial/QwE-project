from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.crud import get_vacancies
from app.schemas import VacancyDB
from app.models import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://utmn.su",
    "https://utmn.su",
    "http://api.utmn.su",
    "https://api.utmn.su",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/vacancies/", response_model=list[VacancyDB])
def get_all_vacansies(limit: int = 100):
    return get_vacancies(limit=limit)
