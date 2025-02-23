from odmantic import Model, Field, Reference
from app.models.Client import Client

class Pet(Model):
    client: Client = Reference()
    name: str = Field(unique=True)
    breed: str
    age: int
    size_in_centimeters: int
