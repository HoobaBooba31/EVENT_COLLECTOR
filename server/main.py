from fastapi import FastAPI
from mongodb.init_db import MongoDBCollections
from PostgreSQL.init_db import BaseRepo, Admins, Permissions
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from routes.api_keyapi import apikey_route
from routes.eventsapi import events_route
from routes.users_dbapi import user_route, engine

load_dotenv()



@asynccontextmanager
async def initialization_db(app: FastAPI):
    """     Initialize the database when the application starts.      """
    try:
        await MongoDBCollections.init_db()
        # ad_repo = BaseRepo(model=Admins)
        # await ad_repo.init_db()
        # perm_repo = BaseRepo(model=Permissions)
        # await perm_repo.init_db()
        yield
    except (IntegrityError, OperationalError) as e:
        print(f"Database initialization error: {e}")
        yield

app = FastAPI(lifespan=initialization_db)
app.include_router(apikey_route)
app.include_router(events_route)
app.include_router(user_route)