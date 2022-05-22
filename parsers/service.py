from settings import settings as s

from .hh_parser import HHParser


def run_vacancies_parser():
    """Парсит вакансии с hh.ru"""
    hh = HHParser(s.app.hh_api_url, 100)
    hh.get_all_vacancies_data()


def run_regions_parser():
    """Парсит и соотносит регионы с кодами РФ"""
    hh = HHParser(s.app.hh_api_url, 100)
    hh.save_and_get_areas()
