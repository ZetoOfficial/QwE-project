from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Vacancy as VacancyORM
from app.schemas import Vacancy


def get_vacancies(limit: int = 100, db: Session = get_db()) -> list[Vacancy]:
    """Получение всех вакансий

    Args:
        db (Session, optional): дб. Defaults to get_db().

    Returns:
        list[Vacancy]: Список всех вакансий
    """
    return db.query(VacancyORM).limit(limit=limit).all()


def get_vacancy_by_id(vacancy_id: int, db: Session = get_db()) -> Vacancy:
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
    # id = Column(Integer, primary_key=True)
    # name = Column(String)
    # area = Column(String)
    # salary = Column(Integer)
    # experience = Column(String)
    # description = Column(String)
    # key_skills = Column(String)
    # alternate_url = Column(String)

    db_vacancy = get_vacancy_by_id(vacancy.id)
    if not db_vacancy:
        db_vacancy = VacancyORM(id=vacancy.id, name=vacancy.name)
        db.add(db_vacancy)
        db.commit()
        db.refresh(db_vacancy)
    return db_vacancy
