import asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from telegram_bot.handlers import admin_route, client_route

bot = Bot(token="")
dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(admin_route.admin_route, client_route.client_route)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())