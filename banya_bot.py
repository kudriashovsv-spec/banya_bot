import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from managers.banya_manager import BanyaManager
from managers.encyclopedia_manager import EncyclopediaManager
from managers.quiz_manager import QuizManager
from handlers.main_handlers import register_handlers, load_subscriptions, save_subscriptions
from handlers.quiz_handlers import register_quiz_handlers
from datetime import datetime, time, timedelta
from managers.tips_manager import TipsManager



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
tips_mgr = TipsManager()


# Регистрируем хендлеры
register_handlers(dp, banya_mgr, encyclopedia_mgr, quiz_mgr)
register_quiz_handlers(dp, quiz_mgr)


async def daily_advice_sender(bot, tips_mgr):
    while True:
        now = datetime.now()
        target_time = datetime.combine(now.date(), time(hour=10, minute=40))
        if now > target_time:
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)

        subs = load_subscriptions()
        for user_id, info in subs.items():
            if info.get("enabled"):
                advice = tips_mgr.get_random_tip()
                text = advice["text"]

                # --- Проверка выходных ---
                weekday = now.weekday()  # 0=понедельник, 6=воскресенье
                if weekday in [4,5,6]:
                    text += "\n🔥 Сегодня отличный день для посещения бани!"

                # --- Отправка фото или только текста ---
                if advice.get("image"):
                    await bot.send_photo(int(user_id), photo=advice["image"], caption=text)
                else:
                    await bot.send_message(int(user_id), f"💡 Совет дня:\n{text}")

async def main():
    print("Бот запущен")
    asyncio.create_task(daily_advice_sender(bot, tips_mgr))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
