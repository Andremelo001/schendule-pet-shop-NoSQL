from fastapi import FastAPI
from app.routes import ServicesRoutes, PetRoutes

app = FastAPI()

# Rotas para Endpoints

app.include_router(ServicesRoutes.router)
app.include_router(PetRoutes.router)