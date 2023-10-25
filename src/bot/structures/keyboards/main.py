from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    Message,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db import Database

MAIN_MENU_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Хранилище 📁')],
        [KeyboardButton(text='Добавить ➕'),
         KeyboardButton(text='Сгенерировать 🔑')]
    ],
    resize_keyboard=True,
    # one_time_keyboard=True
)


async def get_storage_kb(msg: Message, db: Database) -> InlineKeyboardMarkup:
    async with db.session.begin():
        user = await db.user.get(msg.from_user.id)
        records = user.records

    builder = InlineKeyboardBuilder()
    for record in records:
        builder.add(InlineKeyboardButton(text=record.title, callback_data=f'show_{record.id}'))
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
