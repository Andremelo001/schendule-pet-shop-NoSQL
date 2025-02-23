from fastapi import FastAPI
from app.routes import ServicesRoutes, PetRoutes, ClientRoutes, ScheduleRoutes

app = FastAPI()

# Rotas para Endpoints
app.include_router(ClientRoutes.router)
app.include_router(PetRoutes.router)
app.include_router(ScheduleRoutes.router)
app.include_router(ServicesRoutes.router)


