from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseVacancy(BaseModel):
    name: str
    area: str
    salary: Optional[int]
    experience: str
    description: str
    key_skills: Optional[list[str]]
    published_at: datetime
    alternate_url: str
    archive: bool = False


class Vacancy(BaseVacancy):
    id: int

    class Config:
        orm_mode = True


class VacancyInput(BaseVacancy):
    pass
