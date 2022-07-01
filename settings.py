from logging import DEBUG, FileHandler, StreamHandler, basicConfig, getLogger
from pathlib import Path

from pydantic import BaseModel, BaseSettings
from yaml import safe_load

CONFIG_FILE = str(Path(__file__).parent.absolute()) + "/settings.yaml"
LOGFILE_FILE = str(Path(__file__).parent.absolute()) + "/qwe.log"
basicConfig(
    level=DEBUG,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s",
    handlers=[FileHandler(LOGFILE_FILE), StreamHandler()],
)


class App(BaseModel):
    cache_folder: str
    origins: list[str]


class Postgres(BaseModel):
    host: str
    user: str
    password: str
    database: str
    port: int


class Settings(BaseSettings):
    app: App
    postgres: Postgres


def load_settings(path: Path | str = CONFIG_FILE) -> Settings:
    if isinstance(path, str):
        path = Path(path)
    with path.open() as f:
        return Settings.parse_obj(safe_load(f))
