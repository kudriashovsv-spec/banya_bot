from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def build_quiz_keyboard(question, qid):
    builder = InlineKeyboardBuilder()
    for idx, option in enumerate(question["options"]):
        builder.add(InlineKeyboardButton(text=option, callback_data=f"q{qid}_{idx}"))
    builder.adjust(1)  # 1 кнопка в строке
    return builder.as_markup()
