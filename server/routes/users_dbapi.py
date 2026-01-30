import logging
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PostgreSQL.init_db import BaseRepo
from PostgreSQL.db import Admins, Permissions
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()
user_route = APIRouter(prefix="/users", tags=["users"])
engine = create_async_engine(f'postgresql+asyncpg://postgres:123@{os.getenv("HOST_NAME")}:5432/EVENT_COLLECT')

class UsersSearch(BaseModel):
    id: str | None = None
    offset: int
    limit: int | bool

class UserAdd(BaseModel):
    id: str

@user_route.post("/add")
async def add_user(user_data: UserAdd):
    try:
        user_repo = BaseRepo(model=Permissions)
        await user_repo.insert_user(user_id=user_data.id)
        return {"status_code": 200, "detail": "User added successfully"}
    except Exception as e:
        # Логирование ошибки (если есть логгер)
        # logger.error(f"Error inserting API key: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@user_route.post("/add_admin")
async def add_admin(user_data: UserAdd):
    try:
        admin_repo = BaseRepo(model=Admins)
        await admin_repo.insert_user(user_id=user_data.id)
        return {"status_code": 200, "detail": "Admin added successfully"}
    except Exception as e:
        # Логирование ошибки (если есть логгер)
        # logger.error(f"Error inserting API key: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@user_route.delete("/remove_user")
async def delete_user(user_data: UserAdd):
    try:
        user_repo = BaseRepo(model=Permissions)
        await user_repo.delete_user(user_id=user_data.id)
        return {"status_code": 200, "detail": "User deleted successfully"}
    except Exception as e:
        # Логирование ошибки (если есть логгер)
        # logger.error(f"Error inserting API key: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@user_route.delete("/remove_admin")
async def delete_admin(user_data: UserAdd):
    try:
        admin_repo = await BaseRepo(model=Admins)
        await admin_repo.delete_user(user_id=user_data.id)
        return {"status_code": 200, "detail": "Admin deleted successfully"}
    except Exception as e:
        # Логирование ошибки (если есть логгер)
        # logger.error(f"Error inserting API key: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@user_route.get("/admins")
async def get_admins(user_data: UsersSearch):
    try:
        admin_repo = await BaseRepo(model=Admins)
        admins = await admin_repo.select_users(id=user_data.id, offset=user_data.offset, limit=user_data.limit)
        Admins = [admin.id async for admin in admins]
        return {"status_code": 200, "admins": Admins}
    except Exception as e:
        # Логирование ошибки (если есть логгер)
        # logger.error(f"Error inserting API key: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@user_route.get("/users")
async def get_users(user_data: UsersSearch):
    try:
        user_repo = BaseRepo(model=Permissions)
        users = await user_repo.select_users(id=user_data.id, offset=user_data.offset, limit=user_data.limit)
        User = [user.id async for user in users]
        return {"status_code": 200, "users": User}
    except Exception as e:
        # Логирование ошибки (если есть логгер)
        # logger.error(f"Error inserting API key: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

