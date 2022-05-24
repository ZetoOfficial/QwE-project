from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.crud import get_vacancies
from app.schemas import (
    AreaVacancy,
    ExperienceSalary,
    Filter,
    PreviewInfo,
    SkillsDemand,
    SkillsSalary,
    VacancyDB,
)
from app.services import (
    Downloader,
    coloraise,
    get_experience_salary,
    get_skills_demand,
    get_skills_salary,
    preview_information,
)
from settings import settings as s

