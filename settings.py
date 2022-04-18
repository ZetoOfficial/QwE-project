from yaml import load, SafeLoader
from pydantic import BaseSettings, BaseModel

CONFIG_FILE = "settings.yaml"
with open(CONFIG_FILE, "r") as f:
    cfg = load(f, SafeLoader)


class App(BaseModel):
    hh_api_url: str


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
