from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Query
from odmantic import ObjectId
from app.database import engine
from app.models.Services import Services
from pydantic import BaseModel

class ServiceUpdate(BaseModel):
    duration_in_minutes: int | None = None
    type_service: str | None = None
    price: float | None = None


class CategoryPrice(str, Enum):
    cheap = "cheap services"
    medium = "medium services"
    expensive = "expensive services"


router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.post("/", response_model=Services)
async def create_service(service: Services):
    """Endpoint para criar um novo serviço"""
    existing_service = await engine.find_one(Services, Services.type_service == service.type_service)
    
    if existing_service:
        raise HTTPException(
            status_code=400, detail=f"Serviço {service.type_service} já existe!"
        )
    
    await engine.save(service)
    return service


@router.get("/", response_model=list[Services])
async def read_services(offset: int = 0, limit: int = Query(default=10, le=100)):
    """Endpoint para listar todos os Serviços"""
    services = await engine.find(Services, skip=offset, limit=limit)
    
    if not services:
        raise HTTPException(status_code=404, detail="Nenhum serviço cadastrado")
    
    return services


@router.get("/{service_id}", response_model=Services)
async def read_service_for_id(service_id: str):
    """Endpoint que retorna um serviço a partir de um `service_id` do serviço"""
    service = await engine.find_one(Services, Services.id == ObjectId(service_id))
    
    if not service:
        raise HTTPException(status_code=404, detail=f"Serviço com o ID {service_id} não foi encontrado")
    
    return service


@router.delete("/{service_id}")
async def delete_service(service_id: str):
    """Endpoint que deleta um serviço a partir do `service_id` fornecido"""
    service = await engine.find_one(Services, Services.id == ObjectId(service_id))
    
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não foi encontrado")
    
    await engine.delete(service)
    return {"ok": True}


@router.put("/{service_id}", response_model=Services)
async def update_service(service_id: str, service_update: ServiceUpdate):
    """Atualiza os dados do serviço pelo `service_id`"""
    
    service = await engine.find_one(Services, Services.id == ObjectId(service_id))
    
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    # Atualiza apenas os campos enviados na requisição
    for key, value in service_update.model_dump(exclude_unset=True).items():
        setattr(service, key, value)
    
    await engine.save(service)
    return service


@router.get("/category-price/", response_model=list[Services])
async def get_services_by_category_price(category_price: CategoryPrice):
    """
    Endpoint que retorna os serviços por uma categoria de preço.
    """
    if category_price is CategoryPrice.cheap:
        services = await engine.find(Services, Services.price <= 50)
    elif category_price is CategoryPrice.medium:
        services = await engine.find(Services, (Services.price > 50.0) & (Services.price <= 100.0))
    elif category_price is CategoryPrice.expensive:
        services = await engine.find(Services, (Services.price > 100.0) & (Services.price <= 500.0))
    else:
        raise HTTPException(status_code=400, detail="Categoria de preço inválida")
    
    if not services:
        raise HTTPException(
            status_code=404,
            detail="Nenhum serviço encontrado na faixa de preço selecionada",
        )
    
    return services


@router.get("/total-services/", response_model=int)
async def get_total_services():
    """Endpoint que retorna a quantidade total de serviços cadastrados no sistema"""
    total_services = await engine.count(Services)
    return total_services
