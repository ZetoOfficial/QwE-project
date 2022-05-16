from .hh_parser import HHParser


def run_vacancies_parser():
    """Парсит вакансии с hh.ru"""
    hh = HHParser()
    hh.get_all_vacancies_data()


def run_regions_parser():
    """Парсит и соотносит регионы с кодами РФ"""
    hh = HHParser()
    hh.save_and_get_areas()
