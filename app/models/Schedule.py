from odmantic import Model, Reference
from datetime import datetime
from Services import Services
from Client import Client
from Pet import Pet

class Schedule(Model):
    client: "Client" = Reference()
    pet: "Pet" = Reference()
    services: list[Reference["Services"]]
    date_schedule: datetime
    

