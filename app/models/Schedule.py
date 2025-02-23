from odmantic import Model, Reference
from datetime import datetime
from app.models.Services import Services
from app.models.Client import Client
from app.models.Pet import Pet

class Schedule(Model):
    client: Client = Reference()
    pet: Pet = Reference()
    services: list[Services] = []
    date_schedule: datetime