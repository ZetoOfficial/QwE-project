from csv import DictWriter
from json import loads
from uuid import uuid4

from app.crud import get_vacancies
from app.schemas import VacancyDB


class Downloader:
    _folder: str

    def __init__(self, folder: str):
        self._folder = folder

    def generate_path(self, postfix: str) -> str:
        """Генерация уникального пути для файла"""
        return f"{self._folder}/{uuid4().hex}{postfix}"

    def download_as_csv(self) -> str:
        """Выгрузка в csv формат"""
        vacancies = sorted(
            get_vacancies(),
            key=lambda v: (v.area, v.experience, v.salary),
            reverse=True,
        )
        path = self.generate_path(".csv")
        with open(path, "w") as f:
            writer = DictWriter(f, list(VacancyDB.schema()["properties"].keys()))
            writer.writeheader()
            for vacancy in vacancies:
                writer.writerow(loads(VacancyDB.from_orm(vacancy).json()))
        return path

    def download_as_xlsx(self) -> str:
        """Выгрузка в xlsx формат (потом)"""
        vacancies = get_vacancies()
        path = self.generate_path(".xlsx")
        return path
