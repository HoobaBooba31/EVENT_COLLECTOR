import hashlib
import secrets
import asyncio
from typing import Literal

def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode()).hexdigest()

async def creating_api_key() -> tuple:
    """Creating API key for application curl requests.
        Returns:
            tuple: (api_key, hashed_api_key)"""
    api_key = 'sk_curl_' + secrets.token_urlsafe(32)
    hashed_api = hash_api_key(api_key)
    # with httpx.AsyncClient() as client:
    #     pass
    return (api_key, hashed_api)


if __name__ == "__main__":
    asyncio.run(creating_api_key())