import json
import os

from aiogram import types
from aiogram.filters import Command
from keyboards.main_keyboard import main_menu
from managers.encyclopedia_manager import EncyclopediaManager
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from keyboards.quiz_keyboard import build_quiz_keyboard

SUB_FILE = "data/subscriptions.json"

# --- Функции для работы с подписками ---
def load_subscriptions():
    if os.path.exists(SUB_FILE):
        with open(SUB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_subscriptions(subs):
    with open(SUB_FILE, "w", encoding="utf-8") as f:
        json.dump(subs, f, ensure_ascii=False, indent=4)
        

def register_handlers(dp, banya_mgr, encyclopedia_mgr, quiz_mgr):
    @dp.message(Command("start"))
    async def start(message: types.Message):
        await message.answer("Привет! Выбери действие:", reply_markup=main_menu())

    @dp.callback_query(lambda c: c.data == "encyclopedia")
    async def encyclopedia_cb(query: types.CallbackQuery):
        topics = encyclopedia_mgr.get_all_topics()
        builder = InlineKeyboardBuilder()
        for idx, t in enumerate(topics, start=1):
            builder.add(InlineKeyboardButton(text=t["title"], callback_data=f"topic_{idx}"))
        builder.adjust(1)  # 1 кнопка в строке
        kb = builder.as_markup()
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

    @dp.callback_query(lambda c: c.data == "quiz")
    async def quiz_cb(query: types.CallbackQuery):
        question = quiz_mgr.get_question(0)
        if question:
            kb = build_quiz_keyboard(question, 0)
            await query.message.answer(question["question"], reply_markup=kb)
        await query.answer()

    @dp.callback_query(lambda c: c.data == "daily_advice")
    async def daily_advice_cb(query):
        user_id = str(query.from_user.id)
        subs = load_subscriptions()
        enabled = subs.get(user_id, {}).get("enabled", False)

        if enabled:
            subs[user_id]["enabled"] = False
            await query.message.answer("❌ Автосовет дня отключен")
        else:
            subs[user_id] = subs.get(user_id, {})
            subs[user_id]["enabled"] = True
            await query.message.answer("✅ Автосовет дня включен. Совет будет приходить каждый день в 17:00")

        save_subscriptions(subs)
        await query.answer()
