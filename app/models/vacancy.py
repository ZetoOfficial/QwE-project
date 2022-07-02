from sqlalchemy import ARRAY, Boolean, Column, Date, Integer, String

from .base import Base


class Vacancy(Base):
    __tablename__ = "vacancy"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    area = Column(String)
    salary = Column(Integer)
    experience = Column(String)
    description = Column(String)
    key_skills = Column(ARRAY(String))
    published_at = Column(Date)
    archive = Column(Boolean, default=False)
    alternate_url = Column(String)
