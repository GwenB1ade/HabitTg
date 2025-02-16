import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import settings
from database import create_db

from bot.routers.commands import router as commands_router
from bot.routers.creating_habit import router as creating_habit_router
from bot.routers.view_habits import router as view_habits_router
from bot.routers.delete_habit import router as delete_habit_router
from bot.routers.callback import router as callbacks_router

from tasks.tasks import start_sending_all_habits
from service.habit_service import HabitService

bot = Bot(settings.BOT_KEY)
dp = Dispatcher()


async def main():
    dp.include_routers(
        commands_router,
        creating_habit_router,
        view_habits_router,
        delete_habit_router,
        callbacks_router
    )
    create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    create_db()
    logging.basicConfig(level = logging.DEBUG ,
                        format = '%(asctime)s %(levelname)s %(message)s')
    asyncio.run(main())