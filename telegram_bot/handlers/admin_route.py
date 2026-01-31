from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Filter
from telegram_bot.fsm.admin_fsm import UserListStates
from telegram_bot.requests_func import admin_req
from telegram_bot.keyboards.admin_keyboards import admin_keyboard as ad_kb
from telegram_bot.bot_instanse import bot


admin_route = Router()


class AdminsFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        admin = await admin_req.check_admin(message.from_user.id)
        return bool(admin)

# Список админов
@admin_route.message(Command("admin"), AdminsFilter())
async def admin_commands(message: Message):
    await message.answer("""Список команд для админов:
                         /count_users - Количество пользователей
                         /add_user - Добавить пользователя, которые могут пользоваться платформоф
                         /remove_user - Удалить пользователя, который мог платформой
                         /get_user - Получить информацию о конкретном пользователе по ID
                         /get_users - Получить список пользователей с пагинацией""", 
                         reply_markup=ad_kb)

# Подсчет количества пользователей
@admin_route.message(Command("count_users"), AdminsFilter()) 
async def get_count_users(message: Message):
    User = await admin_req.get_users()
    count_of_users = len(User)
    message.answer(f"Количество пользователей, использующих данный сервис {count_of_users}")

# Добавление пользователя
@admin_route.message(Command("add_user"), AdminsFilter()) 
async def add_user(message: Message):
    await message.answer("Введите ID пользователя, которого хотите добавить:")
    await UserListStates.AddUserID.set()


@admin_route.message(UserListStates.AddUserID, AdminsFilter())
async def adding_user_with_concrete_id(message: Message, state: FSMContext):
    await admin_req.add_user(user_id=message.text)
    await message.answer(f"Пользователь с ID {message.text} был добавлен.")
    await state.clear()

# Удаление пользователя
@admin_route.message(Command("remove_user"), AdminsFilter()) 
async def remove_user(message: Message, state: FSMContext):
    await message.answer("Введите ID пользователя, которого хотите удалить:")
    await state.set_state(UserListStates.GetUserIDToRemove)


@admin_route.message(UserListStates.GetUserIDToRemove, AdminsFilter())
async def removing_user_with_concrete_id(message: Message, state: FSMContext):
    await admin_req.remove_user(user_id=message.text)
    await message.answer(f"Пользователь с ID {message.text} был удален.")
    await state.clear()


#Получение одного пользователя в БД
@admin_route.message(Command("get_user"), AdminsFilter())
async def get_user(message: Message, state: FSMContext):
    await message.answer("Введите ID пользователя, которого хотите получить:")
    await state.set_state(UserListStates.GetUserIDForFetch)


@admin_route.message(UserListStates.GetUserIDForFetch)
async def getting_user_with_concrete_id(message: Message, state: FSMContext):
    user = await admin_req.get_users(user_id=int(message.text), offset=0, limit=1)
    if user:
        user_info = user[0]
        await message.answer(f"Информация о пользователе:\nID: {user_info['id']}\nUsername: {user_info.get('username', 'N/A')}")
    else:
        await message.answer(f"Пользователь с ID {message.text} не найден.")
    await state.clear()


# Получение списка пользователей с пагинацией
@admin_route.message(Command("get_users"), AdminsFilter())
async def get_users_list(message: Message, state: FSMContext):
    await message.answer("Для получения списка пользователей введите смещение (offset):")
    await state.set_state(UserListStates.GetOffset)


@admin_route.message(UserListStates.GetOffset, AdminsFilter())
async def get_offset(message: Message, state: FSMContext):
    if message.text == "/cancel" or message.text == "0":
        await state.clear()
        await message.answer("Операция отменена.")
        return await admin_commands(message)
    elif message.text.isdigit():
        await state.update_data(offset=int(message.text))
        await message.answer("Теперь введите лимит (limit):")
        await state.set_state(UserListStates.GetLimit)
    else:
        await message.answer("Пожалуйста, введите корректное числовое значение для смещения (offset) или /cancel для отмены.")
        return


@admin_route.message(UserListStates.GetLimit, AdminsFilter())
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


@admin_route.callback_query(F.data.startswith("approve_"), AdminsFilter())
async def approve_permission(callback_query: CallbackQuery):
    user_id = callback_query.data.split("_")[1]
    await admin_req.add_user(user_id=int(user_id))
    await callback_query.message.answer(f"Пользователю с ID {user_id} было предоставлено разрешение на использование платформы.")
    await callback_query.answer("Разрешение предоставлено.")
    await bot.send_message(
        chat_id=user_id,
        text="Ваш запрос на использование платформы был одобрен администратором."
    )


@admin_route.callback_query(F.data.startswith("deny_"), AdminsFilter())
async def deny_permission(callback_query: CallbackQuery):
    user_id = callback_query.data.split("_")[1]
    await callback_query.message.answer(f"Запрос пользователя с ID {user_id} на использование платформы был отклонен.")
    await callback_query.answer("Запрос отклонен.")
    await bot.send_message(
        chat_id=user_id,
        text="Ваш запрос на использование платформы был отклонен администратором."
    )