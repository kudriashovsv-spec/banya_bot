from aiogram import types
from aiogram.filters import Command
from managers.quiz_manager import QuizManager
from keyboards.quiz_keyboard import build_quiz_keyboard

def register_quiz_handlers(dp, quiz_mgr: QuizManager):
    @dp.message(Command("quiz"))
    async def start_quiz(message: types.Message):
        question = quiz_mgr.get_question(0)
        if question:
            kb = build_quiz_keyboard(question, 0)
            await message.answer(question["question"], reply_markup=kb)

    @dp.callback_query(lambda c: c.data.startswith("q"))
    async def quiz_answer_cb(query: types.CallbackQuery):
        qid, choice = map(int, query.data[1:].split("_"))  # убираем 'q' и парсим числа
        question = quiz_mgr.get_question(qid)
        correct = question["answer"]
        
        if choice == correct:
            text = "✅ Верно!"
        else:
            text = f"❌ Неверно! Правильный ответ: {question['options'][correct]}"
        
        await query.message.answer(text)
        await query.answer()
