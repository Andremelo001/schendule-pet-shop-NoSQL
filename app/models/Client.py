from odmantic import Model, Field

class Client(Model):
    name: str
    cpf: str = Field(unique=True)
    age: int
    is_admin: bool
