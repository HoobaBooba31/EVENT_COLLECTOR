from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="/admin"),
        KeyboardButton(text="/add_user"),
        KeyboardButton(text="/remove_user")
    ],
    [
        KeyboardButton(text="/count_users"),
        KeyboardButton(text="/get_user"),
        KeyboardButton(text="/get_users"),
    ],
], resize_keyboard=True)