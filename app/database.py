from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import settings as s

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    s.postgres.user,
    s.postgres.password,
    s.postgres.host,
    s.postgres.port,
    s.postgres.database,
)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True if s.app.env == "DEV" else False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
metadata = MetaData()
