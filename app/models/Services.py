from odmantic import Model
from pydantic import BaseModel

class Services(Model):
    duration_in_minutes: int
    type_service: str
    price: float

class ServiceUpdate(BaseModel):
    duration_in_minutes: int | None = None
    type_service: str | None = None
    price: float | None = None