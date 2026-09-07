from pydantic import BaseModel

class Hotspot(BaseModel):
    id: int
    lat: float
    lng: float
    lst: float
    ndvi: float
    built_up: float
    population: float
    risk: float
