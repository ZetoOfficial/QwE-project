from sqlalchemy import Column, Integer, String

from .base import Base


class Area(Base):
    __tablename__ = "area"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    region = Column(String)
    city = Column(String)
