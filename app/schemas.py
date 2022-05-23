from typing import Optional

from pydantic import BaseModel, Field


class AreaModel(BaseModel):
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
    total: Optional[int] = None


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
    area: AreaModel
    salary: Optional[Salary]
    experience: Experience
    description: str
    key_skills: Optional[list[Skill]]
    alternate_url: str


class Filter(BaseModel):
    area: Optional[list[str]] = None
    salary: Optional[tuple[int, int]] = None
    experience: Optional[list[str]] = None


class Vacancies(BaseModel):
    items: list[dict]
    found: int
    pages: int
    per_page: int
    page: int
    alternate_url: str


class Area(BaseModel):
    id: int
    code: Optional[str]
    region: str
    city: str


class City(BaseModel):
    code: str
    region: str


class AreaVacancy(BaseModel):
    city: City
    cnt: int
    color: str

    class Config:
        orm_mode = True


class SkillsDemand(BaseModel):
    name: str
    value: int


class SkillsSalary(BaseModel):
    len_skills: list[int]
    salary: list[int]


class PreviewInfo(BaseModel):
    average_salary: int
    average_exp: str
    average_skills_names: str
    average_skills_len: int


class ExperienceSalary(BaseModel):
    exp_names: list[str]
    avr_salary: list[int]
