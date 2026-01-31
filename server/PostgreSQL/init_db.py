from typing import Type
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy import select, delete, inspect, update
from PostgreSQL.db import Admins, Permissions, Base
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_async_engine(f'postgresql+asyncpg://postgres:123@{os.getenv("HOST_NAME")}:5432/EVENT_COLLECT', echo=True)



class BaseRepo:
    def __init__(self, model: Type[DeclarativeMeta]):
        self.model = model
        self.engine = engine

    async def init_db(self):
        """Create table for this model if it doesn't exist."""
        async with engine.begin() as conn:
            def create_tables(sync_conn):
                inspector = inspect(sync_conn)
                if self.model.__tablename__ not in inspector.get_table_names():
                    Base.metadata.create_all(sync_conn)
            await conn.run_sync(create_tables)

    async def insert_user(self, user_id: str):
        async with AsyncSession(self.engine) as session:
            async with session.begin():
                session.add(self.model(id=user_id))

    async def delete_user(self, user_id: str):
        async with AsyncSession(self.engine) as session:
            async with session.begin():
                await session.execute(
                    delete(self.model).where(self.model.id == user_id)
                )

    async def select_users(self, id: int | None, offset: int = 20, limit: int = 20):
        """Return: List[Model(...)]"""
        async with AsyncSession(self.engine) as session:
            query = select(self.model)
            if id is not None:
                query = query.where(self.model.id==id)
            if limit != 0:
                query = query.offset(offset).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
        
    
    async def update_user(self, user_id: str, new_data: dict):
        async with AsyncSession(self.engine) as session:
            async with session.begin():
                await session.execute(
                    update(self.model)
                    .where(self.model.id == user_id)
                    .values(**new_data).if_exists(True)
                )