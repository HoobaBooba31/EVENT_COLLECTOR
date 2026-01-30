import httpx


async def check_admin(user_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://server_address/users/admins", params={"id": user_id})
        if response.status_code == 200:
            admins = response.json().get("admins", [])
            return any(admin.get("id") == user_id for admin in admins)
        return False


async def add_user(user_id: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.post("http://server_address/users/add", json={"id": user_id})


async def get_users(user_id: str, offset: int, limit: int | bool) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://server_address/users/list", params={
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
            response = await client.delete("http://server_address/users/remove_user", json={"id": user_id})
        except httpx.HTTPError as e:
            print(f"HTTP error occurred while removing user: {e}")