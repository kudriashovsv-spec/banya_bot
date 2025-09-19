from aiogram import types
from aiogram.filters import Command
from managers.quiz_manager import QuizManager
from keyboards.quiz_keyboard import build_quiz_keyboard_with_back
from keyboards.main_keyboard import main_menu


def register_quiz_handlers(dp, quiz_mgr: QuizManager):

    @dp.message(Command("quiz"))
    async def start_quiz(message: types.Message):
        question = quiz_mgr.get_question(0)
        if question:
            kb = build_quiz_keyboard_with_back(question, 0)
            await message.answer(question["question"], reply_markup=kb)

    # Используем Text фильтр вместо lambda
    @dp.callback_query(lambda c: c.data and c.data.startswith("q"))
    async def quiz_answer_cb(query: types.CallbackQuery):
        qid, choice = map(int, query.data[1:].split("_"))
        question = quiz_mgr.get_question(qid)
        correct = question["answer"]

        await query.message.edit_reply_markup(reply_markup=None)

        if choice == correct:
            text = "✅ Верно!"
        else:
            text = f"❌ Неверно! Правильный ответ: {question['options'][correct]}"

        next_qid = qid + 1
        next_question = quiz_mgr.get_question(next_qid)

        if next_question:
            kb = build_quiz_keyboard_with_back(next_question, next_qid)
            await query.message.answer(
                f"{text}\n\nСледующий вопрос:\n{next_question['question']}",
                reply_markup=kb
            )
        else:
            await query.message.answer(f"{text}\n\nВикторина окончена!", reply_markup=main_menu())

        await query.answer()
        