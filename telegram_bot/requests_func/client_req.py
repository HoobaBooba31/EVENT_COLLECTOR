import httpx
import logging

async def send_event_tg(event_type: str, user_id: int) -> None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://server_address/events/event_send_tg", json={
                "event": event_type,
                "service": "telegram_bot",
                "api_key": None,
                "payload": {"tg_user_id": user_id}
            })
            if response.status_code == 200:
                logging.info("Event sent successfully.")
            else:
                logging.error(f"Failed to send event. Status code: {response.status_code}, Response: {response.text}")
        except httpx.HTTPError as e:
            logging.error(f"HTTP error occurred while sending event: {e}")