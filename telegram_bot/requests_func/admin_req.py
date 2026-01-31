import httpx


async def check_admin(user_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/users/admins", params={"id": user_id, "offset": 0, "limit": 0})
        if response.status_code == 200:
            admins = response.json().get("admins", [])
            return bool(admins)
        return False


async def get_admins() -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/users/admins", params={ "offset": 0, "limit": 0})
        if response.status_code == 200:
            return response.json().get("admins", [])
        return []
    

async def add_user(user_id: int) -> None:
    async with httpx.AsyncClient() as client:
        await client.post("http://localhost:8000/users/add", json={"id": int(user_id)})


async def get_users(user_id: int, offset: int, limit: int) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/users/users", params={
            "id": user_id,
            "offset": offset,
            "limit": limit
        })
        if response.status_code == 200:
            return response.json().get("users", [])
        return []
    

async def remove_user(user_id: int) -> None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete("http://localhost:8000/users/remove_user", json={"id": user_id})
        except httpx.HTTPError as e:
            print(f"HTTP error occurred while removing user: {e}")