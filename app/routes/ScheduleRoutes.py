from fastapi import APIRouter, HTTPException, Query
from app.database import get_engine
from odmantic import ObjectId
from datetime import datetime
from bson.errors import InvalidId

from app.models.Client import Client
from app.models.Pet import Pet
from app.models.Services import Services
from app.models.Schedule import Schedule, ScheduleCreateRequest, ScheduleUpdate

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"], 
)

engine = get_engine()

@router.post("/", response_model=Schedule)
async def create_schedule(schedule_data: ScheduleCreateRequest) -> Schedule:
    client = await engine.find_one(Client, Client.id == ObjectId(schedule_data.client_id))

    if not client:
        raise HTTPException(status_code=404, detail=f"Cliente com id {schedule_data.client_id} não encontrado")

    pet = await engine.find_one(Pet, Pet.id == ObjectId(schedule_data.pet_id))
    if not pet or pet.client.id != client.id:
        raise HTTPException(status_code=400, detail="Pet não encontrado ou não pertence ao cliente")

    service_ids = []
    for service_id in schedule_data.service_ids:
        service = await engine.find_one(Services, Services.id == ObjectId(service_id))
        if not service:
            raise HTTPException(status_code=404, detail=f"Serviço com id {service_id} não encontrado")
        service_ids.append(service.id) 

    new_schedule = Schedule(
        client=client,
        pet=pet,
        services=service_ids,
        date_schedule=schedule_data.date_schedule
    )

    await engine.save(new_schedule)

    return new_schedule

@router.get("/Get/All", response_model=list[Schedule])
async def get_all_schedules(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0, le=100)) -> list[Schedule]:

    schedules = await engine.find(Schedule, skip=skip, limit=limit)

    return schedules

@router.get("/{schedule_id}", response_model=Schedule)
async def get_schedule_by_id(schedule_id: str) -> Schedule:

    schedule = await engine.find_one(Schedule, Schedule.id == ObjectId(schedule_id))

    if not schedule:
        raise HTTPException(status_code=404, detail=f"Agendamento com o id {schedule_id} não encontrado")

    return schedule

@router.delete("/{schedule_id}", response_model=dict)
async def delete_schedule_by_id(schedule_id: str) -> dict:

    schedule = await engine.find_one(Schedule, Schedule.id == ObjectId(schedule_id))

    if not schedule:
        raise HTTPException(status_code=404, detail=f"Agendamento com o id {schedule_id} não encontrado")
    
    await engine.delete(schedule)

    return {"message": "Agendamento excluido com sucesso"}

@router.put("/{schedule_id}", response_model=Schedule)
async def update_schedule_by_id(schedule_id: str, update_schedule: ScheduleUpdate) -> Schedule:

    schedule = await engine.find_one(Schedule, Schedule.id == ObjectId(schedule_id))

    if not schedule:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    for key, value in update_schedule.model_dump(exclude_unset=True).items():
            setattr(schedule, key, value)

    await engine.save(schedule)

    return schedule

@router.get("/", response_model=Schedule)
async def get_schedules_by_month(month: int, year: int) -> Schedule:

    try:
        # Define o intervalo de datas (início e fim do mês)
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Data inválida. Verifique o ano e o mês informados."
        )

    # Busca os agendamentos no intervalo de datas
    schedules = await engine.find(
        Schedule,
        Schedule.date_schedule >= start_date,
        Schedule.date_schedule < end_date
    )

    if not schedules:
        raise HTTPException(
            status_code=404, detail=f"Nenhum agendamento encontrado para {month}/{year}"
        )
    
    return schedules

@router.get("/total/schedules", response_model=dict)
async def total_schedules() -> dict:
    """Endpoint que retorna o total de agendamentos cadastrados"""
    total_schedules = await engine.count(Schedule)

    return {"total_schedules": total_schedules}




