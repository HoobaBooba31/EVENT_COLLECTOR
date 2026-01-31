import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from telegram_bot.handlers.admin_route import admin_route
from telegram_bot.handlers.client_route import client
from telegram_bot.bot_instanse import bot


dp = Dispatcher(storage=MemoryStorage())
dp.include_routers(admin_route, client)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())