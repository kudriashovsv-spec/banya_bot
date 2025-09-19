from aiogram import types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="📖 Энциклопедия", callback_data="encyclopedia"),
        InlineKeyboardButton(text="📝 Викторина", callback_data="quiz"),
        InlineKeyboardButton(text="💡 Автосовет дня", callback_data="daily_advice"),
        InlineKeyboardButton(text="❓ Помощь", callback_data="help")
    )
    builder.adjust(2)  # 2 кнопки в строке
    return builder.as_markup()


def encyclopedia_menu(topics):
    builder = InlineKeyboardBuilder()
    for idx, t in enumerate(topics, start=1):
        builder.add(InlineKeyboardButton(text=t["title"], callback_data=f"topic_{idx}"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main"))
    builder.adjust(1)  # 1 кнопка в строке
    return builder.as_markup()
