from fastapi import FastAPI
from routes import ClientRoutes

app = FastAPI()

# Rotas para Endpoints
app.include_router(ClientRoutes.router)
