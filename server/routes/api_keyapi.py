import logging
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from datetime import timezone, datetime, timedelta
from security.api_keys import creating_api_key
from mongodb.init_db import MongoDBCollections


apikey_route = APIRouter(prefix="/api_key", tags=["api_key"])

class APIKeyResponseModel(BaseModel):
    api_key: str

@apikey_route.get("/create", response_model=APIKeyResponseModel)
async def put_api_key():
    api_key, hashed_api_key = creating_api_key()
    try:
        ApiCollection = MongoDBCollections("api_keys")
        await ApiCollection.insert_data({"api_key_hash": hashed_api_key,
                                "expired_at": datetime.now(timezone.utc) + timedelta(hours=1),
                                "revoked": False})
        return {"api_key": api_key}
    except Exception as e:
        print(e)
        # Логирование ошибки (если есть логгер)
        # logger.error(f"Error inserting API key: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




