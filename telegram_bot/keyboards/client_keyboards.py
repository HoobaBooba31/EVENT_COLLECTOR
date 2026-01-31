from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

client_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="/help")
    ],
    [
        KeyboardButton(text="/create_event"),
        KeyboardButton(text="/create_ticket")
    ],
], resize_keyboard=True)