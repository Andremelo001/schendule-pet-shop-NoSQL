from odmantic import Model, Field
from pydantic import BaseModel

class Client(Model):
    name: str
    cpf: str = Field(unique=True)
    age: int
    is_admin: bool

class UpdateClient(BaseModel):
    name: str | None
    cpf: str | None
    age: int | None
    is_admin: bool | None
