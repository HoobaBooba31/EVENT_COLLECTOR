from pymongo import ASCENDING, DESCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Literal, Mapping, Any
import db
import json

database: AsyncIOMotorDatabase = db.get_db()

class MongoDBCollections:


    def __init__(self, collection: Literal["api_keys", "events"]):
        self.col = database[collection]


    @staticmethod
    async def init_db() -> bool:

        """     Initialize the database by creating necessary collections.      """
        collections = await database.list_collection_names()

        if "api_keys" not in collections:
            await database.create_collection("api_keys")

        if "events" not in collections:
            await database.create_collection("events")

        await database.api_keys.create_index(
            [("key_hash", ASCENDING)],
            unique=True
        )
        await database.api_keys.create_index(
            [("created_at", DESCENDING)]
        )
        await database.api_keys.create_index(
            [("revoked", ASCENDING)]
        )

        await database.events.create_index(
            [("created_at", DESCENDING)]
        )
        await database.events.create_index(
            [("api_key_id", ASCENDING)]
        )
        await database.events.create_index(
            [("service", ASCENDING)]
        )
        return True


    async def insert_data(self, data: Mapping[str, Any]):
        await self.col.insert_one(data)


    async def select_data(self, data: Mapping[str, Any]):
        res = await self.col.find_one(data)
        if res is None:
            raise ValueError("Data not found")
        return res
    

    async def update_data_revoke(self, _id: str):
        await self.col.update_one({"_id": _id},
                                  {"revoked": True})


    async def delete_all_data(self):
        await self.col.delete_many({})