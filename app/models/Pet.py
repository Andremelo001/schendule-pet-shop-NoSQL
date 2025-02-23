from odmantic import Model, Field, Reference
from app.models.Client import Client
from pydantic import BaseModel
from typing import Optional


class Pet(Model):
    client: Client = Reference()
    name: str = Field(unique=True)
    breed: str
    age: int
    size_in_centimeters: int

class PetUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    size_in_centimeters: Optional[int] = None

