import json
import os

from aiogram import types
from aiogram.filters import Command
from keyboards.main_keyboard import main_menu, encyclopedia_menu
from managers.encyclopedia_manager import EncyclopediaManager
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from keyboards.quiz_keyboard import build_quiz_keyboard_with_back

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

    @dp.callback_query(lambda c: c.data)
    async def callback_handler(query: types.CallbackQuery):
        data = query.data

        # Главное меню
        if data == "main":
            await query.message.edit_text("Привет! Выбери действие:", reply_markup=main_menu())
            await query.answer()

        # Энциклопедия
        elif data == "encyclopedia":
            topics = list(encyclopedia_mgr.get_all_topics())
            kb = encyclopedia_menu(topics)
            await query.message.edit_text("Выберите тему:", reply_markup=kb)
            await query.answer()

        # Факт по теме
        elif data.startswith("topic_"):
            topic_id = int(data.split("_")[1])
            info = encyclopedia_mgr.get_topic_info(topic_id)
            kb = encyclopedia_menu(list(encyclopedia_mgr.get_all_topics()))
            await query.message.edit_text(f"📖 {info}", reply_markup=kb)
            await query.answer()

        # Викторина
        elif data == "quiz":
            question = quiz_mgr.get_question(0)
            if question:
                kb = build_quiz_keyboard_with_back(question, 0)
                await query.message.edit_text(question["question"], reply_markup=kb)
            await query.answer()

        # Автосовет
        elif data == "daily_advice":
            user_id = str(query.from_user.id)
            subs = load_subscriptions()
            enabled = subs.get(user_id, {}).get("enabled", False)

            if enabled:
                subs[user_id]["enabled"] = False
                await query.message.edit_text("❌ Автосовет дня отключен", reply_markup=main_menu())
            else:
                subs[user_id] = subs.get(user_id, {})
                subs[user_id]["enabled"] = True
                await query.message.edit_text("✅ Автосовет дня включен. Совет будет приходить каждый день в 17:00", reply_markup=main_menu())

            save_subscriptions(subs)
            await query.answer()

        # Помощь
        elif data == "help":
            await query.message.edit_text(
                "Список команд:\n/start — старт\nКнопки ниже — действия",
                reply_markup=main_menu()
            )
            await query.answer()
