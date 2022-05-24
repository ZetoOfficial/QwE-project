from dataclasses import dataclass


@dataclass
class AreaDTO:
    code: str
    region: str
    city: str
