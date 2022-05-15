from settings import settings as s
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    s.postgres.user,
    s.postgres.password,
    s.postgres.host,
    s.postgres.port,
    s.postgres.database,
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine)

Base = declarative_base()


def get_db():
    """Получение сессии бд"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
