from pydantic import BaseModel


class BaseArea(BaseModel):
    code: str
    region: str
    city: str


class Area(BaseArea):
    id: int

    class Config:
        orm_mode = True


class AreaInput(BaseArea):
    pass


class City(BaseModel):
    code: str
    region: str


class AreaColor(BaseModel):
    city: City
    cnt: int
    color: str

    class Config:
        orm_mode = True
