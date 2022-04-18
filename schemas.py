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
    start: Optional[int] = Field(None, alias="from")
    to: Optional[int]
    currency: Optional[str]
    gross: Optional[bool]


class Skill(BaseModel):
    name: str


class Vacancy(BaseModel):
    id: str
    name: str
    area: Optional[Area]
    salary: Optional[Salary]
    experience: Optional[Experience]
    description: Optional[str]
    key_skills: Optional[list[Skill]]
    alternate_url: Optional[str]


class VacancyOut(Vacancy):
    """Person model used for serialization."""

    class Config:
        json_encoders = {
            "area": lambda a: a.name,
            "salary": lambda s: (s.start or 0 + s.to or 0) + 80
            if s.currency == "USD"
            else s.start or 0 + s.to or 0,
            "experience": lambda e: e.name,
        }


class Vacancies(BaseModel):
    items: list[Vacancy]
    found: int
    pages: int
    per_page: int
    page: int
    alternate_url: str
