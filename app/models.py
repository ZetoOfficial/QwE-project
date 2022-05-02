from sqlalchemy import Column, Integer, String, ARRAY

from app.database import Base


class Vacancy(Base):
    __tablename__ = "vacancy"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    area = Column(String)
    salary = Column(Integer)
    experience = Column(String)
    description = Column(String)
    key_skills = Column(ARRAY(String))
    alternate_url = Column(String)


class Area(Base):
    __tablename__ = "area"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    region = Column(String)
    city = Column(String)
