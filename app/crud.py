from typing import Optional

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Area as AreaORM
from app.models import Vacancy as VacancyORM
from app.schemas import Area, Filter, Vacancy
from settings import getLogger

logger = getLogger(__name__)


def get_vacancies(
    limit: int = 0, offset: int = 0, filter_: Filter = None, db: Session = get_db()
) -> list[Vacancy]:
    """Получение всех вакансий

    Args:
        limit (int, optional): Лимитированное кол-во элементов. По умолчанию 0.
        offset (int, optional): Смещение. По умолчанию 0.
        filter_ (Filter, optional): Фильтры для вакансий. По умолчанию их нет.

    Returns:
        list[Vacancy]: Список собранных вакансий
    """
    vacancies = db.query(VacancyORM).filter(
        VacancyORM.key_skills.is_not(None), VacancyORM.salary.is_not(None)
    )
    if filter_:
        if salary := filter_.salary:
            vacancies = vacancies.filter(VacancyORM.salary.in_(range(*salary)))
        if experience := filter_.experience:
            vacancies = vacancies.filter(VacancyORM.experience.in_(experience))
        if area := filter_.area:
            vacancies = vacancies.filter(VacancyORM.area.in_(area))
    if limit:
        vacancies = vacancies.limit(limit)
    if offset:
        vacancies = vacancies.offset(offset)
    return vacancies.all()


def get_vacancies_for_areas(db: Session = get_db()):
    """Получение регионов с их кодами РФ от вакансий"""
    return (
        db.query(VacancyORM, AreaORM)
        .with_entities(AreaORM.code, AreaORM.region)
        .filter(VacancyORM.area == AreaORM.city)
        .order_by(AreaORM.code.desc())
        .all()
    )


def get_exp_and_salary(db: Session = get_db()):
    """Получение опыта и заработной платы от вакансий"""
    return (
        db.query(VacancyORM)
        .with_entities(VacancyORM.experience, VacancyORM.salary)
        .filter(VacancyORM.salary.is_not(None))
        .all()
    )


def get_all_skills(limit: int = 0, db: Session = get_db()):
    """Получение навыков и зарплаты от вакансий"""
    skills = (
        db.query(VacancyORM)
        .with_entities(VacancyORM.key_skills, VacancyORM.salary)
        .filter(VacancyORM.key_skills.is_not(None), VacancyORM.salary.is_not(None))
    )
    if limit:
        skills = skills.limit(limit=limit)
    return skills.all()


def get_vacancy_by_id(vacancy_id: int, db: Session = get_db()) -> Optional[Vacancy]:
    """Получение вакансии по идентификатору"""
    return db.query(VacancyORM).filter(VacancyORM.id == vacancy_id).first()


def create_vacancy(vacancy: Vacancy, db: Session = get_db()) -> Vacancy:
    """Создание вакансии"""
    db_vacancy = get_vacancy_by_id(vacancy.id)
    if not db_vacancy:
        if salary := vacancy.salary:
            num = (salary.start or 0) + (salary.to or 0)
            salary = num if (vacancy.salary.currency == "RUR") else num * 60
        db_vacancy = VacancyORM(
            id=vacancy.id,
            name=vacancy.name,
            area=vacancy.area.name,
            salary=salary,
            experience=vacancy.experience.name,
            description=vacancy.description,
            key_skills=[skill.name for skill in vacancy.key_skills]
            if vacancy.key_skills
            else None,
            alternate_url=vacancy.alternate_url,
        )
        db.add(db_vacancy)
        db.commit()
        db.refresh(db_vacancy)
    return db_vacancy


def create_area(area: Area, db: Session = get_db()) -> Area:
    """Создание местности"""
    db_area = get_area_by_city(area.city)
    if not db_area:
        db_area = AreaORM(**(area.dict()))
        db.add(db_area)
        db.commit()
        db.refresh(db_area)
    return db_area


def get_area_by_city(city: str, db: Session = get_db()) -> Area:
    """Получение местности по городу"""
    return db.query(AreaORM).filter(AreaORM.city == city).first()


def get_areas_by_code(code: str, db: Session = get_db()) -> list[Area]:
    """Получение местностей по коду"""
    return db.query(AreaORM).filter(AreaORM.code == code).all()


def update_vacancy(vacancy: Vacancy, db: Session = get_db()) -> Optional[Vacancy]:
    """Обновление существующей вакансии"""
    db_vacancy = get_vacancy_by_id(vacancy_id=vacancy.id)
    if db_vacancy:
        db_vacancy.description = vacancy.description
        ...  # и тд, всё, что нужно изменить
        db.add(db_vacancy)
        db.commit()
        db.refresh(db_vacancy)
    return db_vacancy
