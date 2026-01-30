from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Filter
from server.PostgreSQL.init_db import BaseRepo
from telegram_bot.fsm.client_fsm import UserStates
from telegram_bot.requests_func import client_req

client = Router()


class UserPermissionFilter(Filter):
    def __init__(self, permission_repo: BaseRepo):
        self.permission_repo = permission_repo

    async def __call__(self, message: Message) -> bool:
        permissions = await self.permission_repo.select_users(id=message.from_user.id, offset=0, limit=0)
        return bool(permissions)
    

@client.message(Command("start"))
async def start_command(message: Message):
    await message.answer("""Добро пожаловать! Этот бот работает для сбора событий. 
                        Для разрешения использования, пожалуйста, свяжитесь с администратором.
                        Введите /help для получения списка команд.""")


@client.message(Command("help"))
async def help_command(message: Message):
    await message.answer("""Список доступных команд:
                         /help - Получить список команд""")


@client.message(Command('create_ticket'))
async def create_ticket(message: Message):
    await message.answer("Функция создания тикета в разработке.")


@client.message(Command("create_event"), UserPermissionFilter("Permissions"))
async def create_event(message: Message):
    await message.answer("Введите тип события:")
    await UserStates.EventType.set()


@client.message(UserStates.EventType)
async def get_event_type(message: Message, state: FSMContext):
    event_type = message.text
    await client_req.send_event_tg(event_type=event_type, user_id=message.from_user.id)
    await state.clear()

