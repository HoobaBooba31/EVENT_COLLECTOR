import logging
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Filter
from telegram_bot.fsm.client_fsm import UserStates
from telegram_bot.requests_func import client_req
from telegram_bot.requests_func.admin_req import get_admins, get_users
from telegram_bot.keyboards.client_keyboards import client_keyboard as cl_kb
from telegram_bot.bot_instanse import bot

client = Router()


class UserPermissionFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        permissions = await get_users(user_id=message.from_user.id, offset=0, limit=1)
        return bool(permissions)
    

@client.message(Command("start"))
async def start_command(message: Message):
    await message.answer("""Добро пожаловать! Этот бот работает для сбора событий. 
                            Для разрешения использования,
                            пожалуйста, свяжитесь с администратором.
                            Введите /help для получения списка команд.""")


@client.message(Command("help"))
async def help_command(message: Message):
    await message.answer("""Список доступных команд:
                         /help - Получить список команд
                         /create_ticket - Создать тикет(разрешение от администратора пользоваться платформой)
                         /create_event - Создать событие, которое отправится в БД""", 
                         reply_markup=cl_kb)


@client.message(Command('create_ticket'))
async def create_ticket(message: Message):
    admins = await get_admins()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Разрешить", callback_data=f"approve_{message.from_user.id}")],
        [InlineKeyboardButton(text="Отклонить", callback_data=f"deny_{message.from_user.id}")]
    ])
    logging.info(admins)
    for admin in admins:
        await bot.send_message(
            chat_id=admin,
            text=f"Пользователь {message.from_user.full_name} (ID: {message.from_user.id}) запрашивает разрешение на использование платформы.",
            reply_markup=keyboard
        )
    await message.answer("Ваш запрос на разрешение использования платформы был отправлен администраторам.")

    


@client.message(Command("create_event"), UserPermissionFilter())
async def create_event(message: Message, state: FSMContext):
    await message.answer("Введите тип события:")
    await state.set_state(UserStates.EventType)


@client.message(UserStates.EventType)
async def get_event_type(message: Message, state: FSMContext):
    event_type = message.text
    await client_req.send_event_tg(event_type=event_type, user_id=message.from_user.id)
    await state.clear()

