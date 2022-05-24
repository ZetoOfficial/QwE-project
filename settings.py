from logging import DEBUG, INFO, FileHandler, StreamHandler, basicConfig, getLogger
from pathlib import Path

from pydantic import BaseModel, BaseSettings
from yaml import SafeLoader, load

CONFIG_FILE = str(Path(__file__).parent.absolute()) + "/settings.yaml"
LOGFILE_FILE = str(Path(__file__).parent.absolute()) + "/qwe.log"
basicConfig(
    level=DEBUG,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s",
    handlers=[FileHandler(LOGFILE_FILE), StreamHandler()],
)


class App(BaseModel):
    hh_api_url: str
    cache_folder: str
    media_folder: str
    env: str


class Postgres(BaseModel):
    host: str
    user: str
    password: str
    database: str
    port: int


class Settings(BaseSettings):
    app: App
    postgres: Postgres


with open(CONFIG_FILE, "r") as f:
    settings = Settings.parse_obj(load(f, SafeLoader))
