import logging
import hashlib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict
from mongodb.init_db import MongoDBCollections
from datetime import datetime, timezone, timedelta


events_route = APIRouter(prefix="/events", tags=["events"])
logging.basicConfig(level=logging.INFO)


class Events(BaseModel):
    event: str
    service: str
    api_key: str
    model_config = ConfigDict(extra="allow")

class EventsTG(BaseModel):
    event: str
    service: str
    model_config = ConfigDict(extra="allow")


@events_route.post("/event_send")
async def log_event(event_data: Events):
    try:
        APIKeyCollection = MongoDBCollections("api_keys")
        api_data = event_data.api_key
        expire = await APIKeyCollection.select_data ({"api_key_hash": hashlib.sha256(api_data.encode()).hexdigest()})

        if expire["expired_at"].replace(tzinfo=timezone.utc) <= datetime.now(timezone.utc) or expire["revoked"] == True:
            try:
                await APIKeyCollection.update_data_revoke(expire["_id"])
            except:
                pass
            raise HTTPException(status_code=403, detail="The API Key was revoked")
        
        else:
                try:
                    EventCollection = MongoDBCollections("events")
                    await EventCollection.insert_data({"event": event_data.event,
                                                "service": event_data.service,
                                                "api_key_id": hashlib.sha256(api_data.encode()).hexdigest(),
                                                "expired_at": datetime.now(timezone.utc) + timedelta(days=1)})

                    return {"status_code": 200, "detail": "Event logged successfully"}
                
                except Exception as e:
                    logging.error(f"Error inserting API key: {e}")
                    raise HTTPException(status_code=500, detail="Internal Server Error")
                
    except Exception as e:
        logging.error(f"Something WRONG, {e}")
        raise HTTPException(status_code=400, detail="API key wasn't found")
    

@events_route.post("/event_send_tg")
async def log_event_tg(event_data: EventsTG):
    try:
        EventCollection = MongoDBCollections("events")
        await EventCollection.insert_data({"event": event_data.event,
                                            "service": event_data.service,
                                            "expired_at": datetime.now(timezone.utc) + timedelta(days=1)})

        return {"status_code": 200, "detail": "Event logged successfully"}
    
    except Exception as e:
        logging.error(f"Error inserting API key: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        

@events_route.get("/select_all")
async def get_all_events():
    try:
        EventCollection = MongoDBCollections("events")
        events = await EventCollection.select_data({})
        return {"status_code": 200, "events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
