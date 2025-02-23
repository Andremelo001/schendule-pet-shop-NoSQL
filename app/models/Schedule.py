from odmantic import Model, Reference, ObjectId
from datetime import datetime
from app.models.Client import Client
from app.models.Pet import Pet
from typing import List
from pydantic import BaseModel

class Schedule(Model):
    client: Client = Reference()
    pet: Pet = Reference()
    services: List[ObjectId]
    date_schedule: datetime

class ScheduleCreateRequest(BaseModel):
    client_id: str
    pet_id: str
    service_ids: List[str]
    date_schedule: datetime

class ScheduleUpdate(BaseModel):
    date_schedule: datetime | None
