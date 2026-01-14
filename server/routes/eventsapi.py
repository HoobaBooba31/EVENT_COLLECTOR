import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mongodb.init_db import MongoDBCollections
from datetime import datetime, timezone, timedelta


events_route = APIRouter(prefix="/events", tags=["events"])

class Events(BaseModel):
    event: str
    payload: dict
    platform: str


@events_route.post("/log")
async def log_event(event_data: Events):
    try:
        APIKeyCollection = MongoDBCollections("api_keys")
        api_data = event_data.payload["api_key"]
        expire = APIKeyCollection.select_data({"api_key": api_data})

        if expire["expired_at"] <= datetime.now(timezone.utc):
            raise HTTPException(status_code=403, detail="The API Key was revoked")
        
        else:
            if Events.platform == "app_curl":
                pass

            else:
                try:
                    EventCollection = MongoDBCollections("events")
                    EventCollection.insert_data({"event": event_data.event,
                                                "payload": {**event_data.payload},
                                                "platform": event_data.platform,
                                                "datetime": datetime.now(timezone.utc) + timedelta(day=1)})

                    return {"status_code": 200, "detail": "Event logged successfully"}
                
                except Exception as e:
                    # Логирование ошибки (если есть логгер)
                    # logger.error(f"Error inserting API key: {e}")
                    raise HTTPException(status_code=500, detail="Internal Server Error")
                
    except Exception as e:
        raise HTTPException(status_code=400, detail="API key wasn't found")


@events_route.get("/select_all")
async def get_all_events():
    try:
        EventCollection = MongoDBCollections("events")
        events = EventCollection.select_data()
        return {"status_code": 200, "events": events}
    except Exception as e:
        # Логирование ошибки (если есть логгер)
        # logger.error(f"Error inserting API key: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
