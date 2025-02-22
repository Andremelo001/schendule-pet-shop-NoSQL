from odmantic import Model

class Services(Model):
    duration_in_minutes: int
    type_service: str
    price: float