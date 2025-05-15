from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends
import os

MONGO_URL = os.getenv("MONGO_URL", "http://127.0.0.1:27017/securedb")

client = AsyncIOMotorClient(MONGO_URL)
db = client.get_default_database()

# Dependency pour injection FastAPI
def get_db() -> AsyncIOMotorDatabase:
    return db
