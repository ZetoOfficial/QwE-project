from pathlib import Path
from yaml import load, SafeLoader
from pydantic import BaseSettings, BaseModel
from logging import basicConfig, getLogger, FileHandler, StreamHandler, INFO, DEBUG

CONFIG_FILE = str(Path(__file__).parent.absolute()) + "/settings.yaml"
LOGFILE_FILE = str(Path(__file__).parent.absolute()) + "/qwe.log"
basicConfig(
    level=INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s",
    handlers=[FileHandler(LOGFILE_FILE), StreamHandler()],
)
with open(CONFIG_FILE, "r") as f:
    cfg = load(f, SafeLoader)


class App(BaseModel):
    hh_api_url: str
    cache_folder: str


class Postgres(BaseModel):
    host: str
    user: str
    password: str
    database: str
    port: int


class Settings(BaseSettings):
    app: App
    postgres: Postgres


settings = Settings.parse_obj(cfg)
