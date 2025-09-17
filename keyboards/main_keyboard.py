from aiogram import types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Энциклопедия бани", callback_data="encyclopedia"),
         InlineKeyboardButton(text="Помощь", callback_data="help")],
        [InlineKeyboardButton(text="Викторина", callback_data="quiz")]  # новая кнопка
    ])
    return kb

def encyclopedia_buttons(topics):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["title"], callback_data=f"topic_{idx+1}")]
        for idx, t in enumerate(topics)
    ])
    return kb

def register_handlers(dp, banya_mgr, encyclopedia_mgr):

    @dp.message(Command("start"))
    async def start(message: types.Message):
        await message.answer("Привет! Выбери действие:", reply_markup=main_menu())

    @dp.callback_query(lambda c: c.data == "encyclopedia")
    async def encyclopedia_cb(query: types.CallbackQuery):
        topics = encyclopedia_mgr.get_all_topics()
        kb = encyclopedia_buttons(list(topics))
        await query.message.answer("Выберите тему:", reply_markup=kb)
        await query.answer()

    @dp.callback_query(lambda c: c.data.startswith("topic_"))
    async def topic_info_cb(query: types.CallbackQuery):
        topic_id = int(query.data.split("_")[1])
        info = encyclopedia_mgr.get_topic_info(topic_id)
        await query.message.answer(f"📖 {info}")
        await query.answer()

    @dp.callback_query(lambda c: c.data == "help")
    async def help_cb(query: types.CallbackQuery):
        await query.message.answer("Список команд:\n/start — старт\nКнопки ниже — действия")
        await query.answer()
