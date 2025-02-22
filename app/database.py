from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# MongoDB connection
DATABASE_URL = os.getenv("url")

client = AsyncIOMotorClient(DATABASE_URL)

db = client["petshop_db"]

engine = AIOEngine(client=client, database="petshop_db")

def get_engine() -> AIOEngine:
    return engine
