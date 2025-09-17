import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from managers.banya_manager import BanyaManager
from managers.encyclopedia_manager import EncyclopediaManager
from managers.quiz_manager import QuizManager
from handlers.main_handlers import register_handlers
from handlers.quiz_handlers import register_quiz_handlers


# Загружаем токен
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаём бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаём менеджеры
banya_mgr = BanyaManager()
encyclopedia_mgr = EncyclopediaManager()
quiz_mgr = QuizManager()

# Регистрируем хендлеры
register_handlers(dp, banya_mgr, encyclopedia_mgr, quiz_mgr)
register_quiz_handlers(dp, quiz_mgr)


async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
