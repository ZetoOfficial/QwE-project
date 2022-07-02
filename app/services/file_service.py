from pandas import DataFrame

from app.schemas import Vacancy
from settings import load_settings

from .vacancy_service import VacancyService

settings = load_settings()


class FileService:
    @staticmethod
    async def get_vacancies_csv_report() -> str:
        vacancies = await VacancyService.get_all_vacancies(0, 0)
        vacancies = list(map(lambda v: Vacancy(**v.__dict__).__dict__, vacancies))
        filepath = settings.app.media_folder + "/vacancies_report.csv"
        pd_df = DataFrame(data=vacancies, columns=Vacancy.__fields__)
        pd_df.to_csv(filepath, sep="\t", index=False, encoding="utf-16")
        return filepath
