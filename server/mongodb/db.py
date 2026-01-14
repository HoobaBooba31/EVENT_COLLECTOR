from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "event_service")

_client: AsyncIOMotorClient | None = None
db = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(MONGO_URI)
    return _client


def get_db() -> AsyncIOMotorDatabase: 
    global db
    if db is None:
        db = get_client()[DB_NAME]
    return db