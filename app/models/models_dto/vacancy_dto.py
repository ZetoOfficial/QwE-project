from dataclasses import dataclass


@dataclass
class VacancyDTO:
    name: str
    area: str
    salary: int
    experience: str
    description: str
    key_skills: list[str]
    alternate_url: str


@dataclass
class CreateVacancyDTO(VacancyDTO):
    id: int


@dataclass
class UpdateVacancyDTO(VacancyDTO):
    pass
