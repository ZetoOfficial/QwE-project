from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import load_settings

settings = load_settings()

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    settings.postgres.user,
    settings.postgres.password,
    settings.postgres.host,
    settings.postgres.port,
    settings.postgres.database,
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=settings.app.environment == "dev")
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
metadata = MetaData()
