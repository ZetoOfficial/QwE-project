from typing import Optional
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Vacancy as VacancyORM
from app.schemas import Vacancy, VacancyDB
from settings import getLogger

logger = getLogger(__name__)


def get_vacancies(limit: int = 100, db: Session = get_db()) -> list[Vacancy]:
    """Получение всех вакансий

    Args:
        db (Session, optional): дб. Defaults to get_db().

    Returns:
        list[Vacancy]: Список всех вакансий
    """
    return db.query(VacancyORM).limit(limit=limit).all()


def get_vacancy_by_id(vacancy_id: int, db: Session = get_db()) -> Optional[Vacancy]:
    """Получение вакансии по идентификатору

    Args:
        vacancy_id (int): идентификатор вакансии
        db (Session, optional): дб. Defaults to get_db().

    Returns:
        Vacancy: вакансия
    """
    return db.query(VacancyORM).filter(VacancyORM.id == vacancy_id).first()


def create_vacancy(vacancy: Vacancy, db: Session = get_db()) -> Vacancy:
    """Создание вакансии

    Args:
        vacancy (Vacancy): вакансия
        db (Session, optional): дб. Defaults to get_db().

    Returns:
        Vacancy: вакансия
    """
    db_vacancy = get_vacancy_by_id(vacancy.id)
    if not db_vacancy:
        if salary := vacancy.salary:
            num = (salary.start or 0) + (salary.to or 0)
            salary = num if (vacancy.salary.currency == "RUR") else num * 76
        db_vacancy = VacancyORM(
            id=vacancy.id,
            name=vacancy.name,
            area=vacancy.area.name,
            salary=salary,
            experience=vacancy.experience.name,
            description=vacancy.description,
            key_skills=[skill.name for skill in skills] if (skills := vacancy.key_skills) else None,
            alternate_url=vacancy.alternate_url,
        )
        db.add(db_vacancy)
        db.commit()
        db.refresh(db_vacancy)
    return db_vacancy
