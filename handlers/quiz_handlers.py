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

    @dp.callback_query()
    async def quiz_answer_cb(query: types.CallbackQuery):
        if not query.data or not query.data.startswith("q"):
            return  # Игнорируем другие callback_data
        qid, choice = map(int, query.data[1:].split("_"))
        question = quiz_mgr.get_question(qid)
        correct = question["answer"]

        # Скрываем кнопки старого вопроса
        await query.message.edit_reply_markup(reply_markup=None)

        # Текст ответа
        if choice == correct:
            text = "✅ Верно!"
        else:
            text = f"❌ Неверно! Правильный ответ: {question['options'][correct]}"

        # Следующий вопрос
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

        # Подтверждаем callback
        await query.answer()
