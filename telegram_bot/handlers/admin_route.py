from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Filter
from telegram_bot.fsm.admin_fsm import UserListStates
from telegram_bot.requests_func import admin_req


ADMINS = {}


admin_route = Router()


class AdminsFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        admin = await admin_req.check_admin(message.from_user.id)
        return bool(admin)

# Список админов
@admin_route.message(Command("admin"), AdminsFilter(admin_repo="Admins"))
async def admin_commands(message: Message):
    await message.answer("Список команд для админов:")

# Подсчет количества пользователей
@admin_route.message(Command("count_users"), AdminsFilter(admin_repo="Admins")) 
async def get_count_users(message: Message):
    User = await admin_req.get_users()
    count_of_users = len(User)
    message.answer(f"Количество пользователей, использующих данный сервис {count_of_users}")

# Добавление пользователя
@admin_route.message(Command("add_user"), AdminsFilter(admin_repo="Admins")) 
async def add_user(message: Message):
    await message.answer("Введите ID пользователя, которого хотите добавить:")
    await UserListStates.GetUserID.set()


@admin_route.message(UserListStates.GetUserID, AdminsFilter(admin_repo="Admins"))
async def adding_user_with_concrete_id(message: Message, state: FSMContext):
    await admin_req.add_user(user_id=message.text)
    await message.answer(f"Пользователь с ID {message.text} был добавлен.")

# Удаление пользователя
@admin_route.message(Command("remove_user"), AdminsFilter(admin_repo="Admins")) 
async def remove_user(message: Message):
    await message.answer("Введите ID пользователя, которого хотите удалить:")
    await UserListStates.GetUserIDToRemove.set()


@admin_route.message(UserListStates.GetUserIDToRemove, AdminsFilter(admin_repo="Admins"))
async def removing_user_with_concrete_id(message: Message, state: FSMContext):
    await admin_req.remove_user(user_id=message.text)
    await message.answer(f"Пользователь с ID {message.text} был удален.")

# Получение списка пользователей с пагинацией
@admin_route.message(Command("get_users"), AdminsFilter(admin_repo="Admins"))
async def get_users_list(message: Message):
    await message.answer("Для получения списка пользователей введите смещение (offset):")
    await UserListStates.GetOffset.set()


@admin_route.message(UserListStates.GetOffset, AdminsFilter(admin_repo="Admins"))
async def get_offset(message: Message, state: FSMContext):
    if message.text == "/cancel" or message.text == "0":
        await state.clear()
        await message.answer("Операция отменена.")
        return await admin_commands(message)
    elif message.text.isdigit():
        await state.update_data(offset=int(message.text))
        await message.answer("Теперь введите лимит (limit):")
        await UserListStates.GetLimit.set()
    else:
        await message.answer("Пожалуйста, введите корректное числовое значение для смещения (offset) или /cancel для отмены.")
        return


@admin_route.message(UserListStates.GetLimit, AdminsFilter(admin_repo="Admins"))
async def get_limit(message: Message, state: FSMContext):
    data = await state.get_data()
    offset = data.get("offset")
    limit = int(message.text)

    users = await admin_req.get_users(user_id=None, offset=offset, limit=limit)

    if users:
        users_list = "\n".join([f"ID: {user.id}, Username: {user.username}" for user in users])
        await message.answer(f"Список пользователей:\n{users_list}")
    else:
        await message.answer("Пользователи не найдены с указанными параметрами.")

    await state.clear()