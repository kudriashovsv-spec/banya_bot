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
            # Сохраняем id текущего вопроса в callback_data
            await message.answer(question["question"], reply_markup=kb)

    @dp.callback_query(lambda c: c.data.startswith("q"))
    async def quiz_answer_cb(query: types.CallbackQuery):
        qid, choice = map(int, query.data[1:].split("_"))  # парсим числа
        question = quiz_mgr.get_question(qid)
        correct = question["answer"]

        # 1️⃣ Формируем текст ответа
        if choice == correct:
            text = "✅ Верно!"
        else:
            text = f"❌ Неверно! Правильный ответ: {question['options'][correct]}"

        # 2️⃣ Получаем следующий вопрос
        next_qid = qid + 1
        next_question = quiz_mgr.get_question(next_qid)

        if next_question:
            # Если есть следующий вопрос — создаем новые кнопки
            kb = build_quiz_keyboard_with_back(next_question, next_qid)
            await query.message.edit_text(
                f"{text}\n\nСледующий вопрос:\n{next_question['question']}",
                reply_markup=kb
            )
        else:
            # Если вопросов больше нет — показываем конец викторины и главное меню
            await query.message.edit_text(
                f"{text}\n\nВикторина окончена!",
                reply_markup=main_menu()
            )

        # 3️⃣ Подтверждаем callback
        await query.answer()
