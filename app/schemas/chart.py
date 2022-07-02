from pydantic import BaseModel


class SkillsDemand(BaseModel):
    name: str
    value: int


class SkillsSalary(BaseModel):
    len_skills: list[int]
    salary: list[int]


class ExperienceSalary(BaseModel):
    exp_names: list[str]
    avr_salary: list[int]


class PreviewInfo(BaseModel):
    average_salary: int
    average_exp: str
    average_skills_names: str
    average_skills_len: int
