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
    id: int
    name: str
    area: Optional[Area]
    salary: Optional[Salary]
    experience: Optional[Experience]
    description: Optional[str]
    key_skills: Optional[list[Skill]]
    alternate_url: Optional[str]


class Vacancies(BaseModel):
    items: list[Vacancy]
    found: int
    pages: int
    per_page: int
    page: int
    alternate_url: str
