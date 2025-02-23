from fastapi import APIRouter, HTTPException, Query
from database import get_engine
from models.Client import Client, UpdateClient
from models.Pet import Pet
from models.Schedule import Schedule
from models.Services import Services
from odmantic import ObjectId

router = APIRouter(
prefix="/clients",
tags=["Clients"], 
)

engine = get_engine()

@router.post("/", response_model=Client)
async def create_client(client: Client) -> Client:

    client_exists = await engine.find_one(Client, Client.cpf == client.cpf)

    if client_exists:
        raise HTTPException(status_code=400, detail=f"O Cliente com o cpf {client.cpf} já foi cadastrado")

    await engine.save(client)
    return client

@router.get("/")
async def get_all_clients(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0, le=100)):

    clients = await engine.find(Client, skip=skip, limit=limit)

    response = []
    
    for client in clients:
        pets = await engine.find(Pet, Pet.client == client.id)
        response.append({
            "client": {
                "id": str(client.id),
                "name": client.name,
                "cpf": client.cpf,
                "age": client.age,
                "is_admin": client.is_admin
            },
            "pets": [{"id": str(pet.id), "name": pet.name, "breed": pet.breed, "age": pet.age, "size_in_centimeters": pet.size_in_centimeters} for pet in pets]
        })
    
    return response


@router.get("/{client_id}")
async def get_client_by_id(client_id: str):

    client = await engine.find_one(Client, Client.id == ObjectId(client_id))

    if not client:
        raise HTTPException(status_code=404, detail=f"Cliente com o id{client_id} não encontrado")
    
    pets = await engine.find(Pet, Pet.client == client.id)
    
    response = {
        "client": {
            "id": str(client.id),
            "name": client.name,
            "cpf": client.cpf,
            "age": client.age,
            "is_admin": client.is_admin
        },
            "pets": [
                {
                    "id": str(pet.id), 
                    "name": pet.name, 
                    "breed": pet.breed, 
                    "age": pet.age, 
                    "size_in_centimeters": pet.size_in_centimeters
                } 
                for pet in pets
            ]
    }
    
    return response

@router.get("/{client_id}")
async def get_clients_schedules_by_id(client_id: str):

    client = await engine.find_one(Client, Client.id == ObjectId(client_id))

    if not client:
        raise HTTPException(status_code=404, detail=f"Cliente com o id{client_id} não encontrado")

    schedules = await engine.find(Schedule, Schedule.client == client.id)

    response = []

    for schedule in schedules:
        pet = await engine.find_one(Pet, Pet.id == schedule.pet.id)

        service_ids = [service.id for service in schedule.services]
        services = await engine.find(Services, Services.id.in_(service_ids))

        response.append({
            "date_schedule": schedule.date_schedule.isoformat(),
            "client": {
                "id": str(client.id),
                "name": client.name,
                "cpf": client.cpf,
                "age": client.age,
                "is_admin": client.is_admin
            },
            "pet": {
                "id": str(pet.id),
                "name": pet.name,
                "breed": pet.breed,
                "age": pet.age,
                "size_in_centimeters": pet.size_in_centimeters
            },
            "services": [
                {
                    "id": str(service.id),
                    "type_service": service.type_service,
                    "duration_in_minutes": service.duration_in_minutes,
                    "price": service.price
                }
                for service in services
            ]
        })

    return response

@router.put("/{client_id}", response_model=Client)
async def update_client_for_id(client_id: str, update_cliente: UpdateClient) -> Client:

    client = await engine.find_one(Client, Client.id == ObjectId(client_id))

    if not client:
        raise HTTPException(status_code=404, detail=f"Cliente com o id {client_id} não encontrado")
    
    for key, value in update_cliente.model_dump(exclude_unset=True).items():
            setattr(client, key, value)

    await engine.save(client)

    return client


@router.delete("/{client_id}")
async def delete_client_for_id(client_id: str) -> dict:
    client = await engine.find_one(Client, Client.id == ObjectId(client_id))

    if not client:
        raise HTTPException(status_code=404, detail=f"Cliente com o {client_id} não encontrado")
    
    try: 
        pets_delete = await engine.find(Pet, Pet.client == client.id)
        for pets in pets_delete:
            await engine.delete(pets)
        
        schedule_delete = await engine.find(Schedule, Schedule.client == client.id)
        for schedules in schedule_delete:
            await engine.delete(schedules)

        await engine.delete(client)

        return {"message": "Cliente deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar cliente e seus dados associados: {str(e)}")




