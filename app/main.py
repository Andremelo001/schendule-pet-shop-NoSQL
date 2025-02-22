from fastapi import FastAPI
from routes import ClientRoutes, PetRoutes, ScheduleRoutes, ServicesRoutes

app = FastAPI()

# Rotas para Endpoints
app.include_router(ClientRoutes.router)
app.include_router(PetRoutes.router)
app.include_router(ScheduleRoutes.router)
app.include_router(ServicesRoutes.router)