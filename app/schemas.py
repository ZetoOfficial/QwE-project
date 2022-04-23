from typing import Optional
from pydantic import BaseModel, Field


class Area(BaseModel):
    id: int
    name: str
    url: str


class Experience(BaseModel):
    id: str
    name: str


class Salary(BaseModel):
    start: Optional[int] = Field(0, alias="from")
    to: Optional[int] = 0
    currency: str
    gross: bool


class Skill(BaseModel):
    name: str


class VacancyDB(BaseModel):
    id: int
    name: str
    area: str
    salary: Optional[int]
    experience: str
    description: str
    key_skills: Optional[list[str]]
    alternate_url: str

    class Config:
        orm_mode = True


class Vacancy(BaseModel):
    id: int
    name: str
    area: Area
    salary: Optional[Salary]
    experience: Experience
    description: str
    key_skills: Optional[list[Skill]]
    alternate_url: str


class Vacancies(BaseModel):
    items: list[dict]
    found: int
    pages: int
    per_page: int
    page: int
    alternate_url: str
