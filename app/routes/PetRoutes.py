from fastapi import APIRouter, HTTPException, Depends, Query
from odmantic import ObjectId
from typing import Optional, List

from app.database import get_engine
from app.models.Pet import Pet, PetUpdate
from app.models.Client import Client
from app.models.Schedule import Schedule


router = APIRouter(
    prefix="/pets",
    tags=["Pets"],
)


@router.post("/{client_id}/pet/", response_model=Pet)
async def create_pet_for_client(client_id: str, pet: Pet):
    """Cria um novo pet associado a um cliente a partir do `client_id`."""
    engine = get_engine()

    client = await engine.find_one(Client, Client.id == ObjectId(client_id))
    if not client:
        raise HTTPException(status_code=404, detail=f"Cliente {client_id} não encontrado")

    existing_pet = await engine.find_one(Pet, Pet.name == pet.name)
    if existing_pet:
        raise HTTPException(
            status_code=400,
            detail=f"O cliente {client_id} já tem um pet com o nome {pet.name} cadastrado"
        )

    pet.client = client
    await engine.save(pet)
    return pet


@router.get("/", response_model=List[Pet])
async def read_pets(offset: int = 0, limit: int = Query(default=10, le=100)):
    """Retorna todos os pets cadastrados, com paginação."""
    engine = get_engine()
    pets = await engine.find(Pet, skip=offset, limit=limit)

    if not pets:
        raise HTTPException(status_code=404, detail="Nenhum pet cadastrado")

    return pets


@router.get("/{client_id}", response_model=List[Pet])
async def read_pet_for_client(client_id: str) -> List[Pet]:
    """Retorna todos os pets associados a um `client_id`."""
    engine = get_engine()

    if not ObjectId.is_valid(client_id):
        raise HTTPException(status_code=400, detail="ID de cliente inválido")

    pets = await engine.find(Pet, Pet.client == ObjectId(client_id))
    if not pets:
        raise HTTPException(status_code=404, detail=f"Nenhum pet encontrado para o cliente {client_id}")

    return pets


@router.delete("/pets/{pet_id}")
async def delete_pet(pet_id: str):
    engine = get_engine()

    if not ObjectId.is_valid(pet_id):
        raise HTTPException(status_code=400, detail="ID do pet inválido")

    pet = await engine.find_one(Pet, Pet.id == ObjectId(pet_id))
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    # Remover agendamentos associados ao pet
    schedules = await engine.find(Schedule, Schedule.pet == pet.id)
    for schedule in schedules:
        await engine.delete(schedule)

    # Remover o pet
    await engine.delete(pet)
    
    return {"ok": True}


@router.put("/{pet_id}")
async def update_pet(pet_id: str, update_data: PetUpdate):
    engine = get_engine()

    # Validar o ID
    if not ObjectId.is_valid(pet_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Buscar o pet pelo ID
    pet = await engine.find_one(Pet, Pet.id == ObjectId(pet_id))
    if not pet:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    # Atualizar os dados do pet
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(pet, key, value)

    await engine.save(pet)
    return pet

@router.get("/{pet_name}/pet-name", response_model=List[Pet])
async def get_pet_by_name(
    pet_name: str,
    client_id: Optional[str] = None,
    offset: int = 0,
    limit: int = Query(default=10, le=100),
):
    """Busca pets por nome parcial ou completo. Se `client_id` for informado, filtra pelos pets do cliente."""
    engine = get_engine()

    # Filtro base para buscar o nome parcialmente correspondente (case insensitive)
    filters = {"name": {"$regex": pet_name, "$options": "i"}}

    if client_id:
        if not ObjectId.is_valid(client_id):
            raise HTTPException(status_code=400, detail="ID do cliente inválido")
        
        client = await engine.find_one(Client, Client.id == ObjectId(client_id))
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        filters["client"] = client.id

    pets = await engine.find(Pet, filters, skip=offset, limit=limit)
    
    if not pets:
        raise HTTPException(status_code=404, detail="Nenhum pet encontrado")

    return pets
