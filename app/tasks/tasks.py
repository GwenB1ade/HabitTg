from celery import Celery
import asyncio
from datetime import datetime, timedelta
from config import settings
import pytz

from aiogram import Bot

from typing import TYPE_CHECKING
from models.habit import DaysEnum

if TYPE_CHECKING:
    from models import HabitModel


celery = Celery(
    'tasks',
    broker = f'amqp://{settings.BROKER_USER}:{settings.BROKER_PASS}@{settings.BROKER_HOST}:{settings.BROKER_PORT}',
    backend = 'rpc://'
)


celery.conf.task_routes = {
    'tasks.send_habit': 'default'
}




async def send_message_for_user_in_tg(message: str, chat_id: int):
    bot = Bot(settings.BOT_KEY)
    await bot.send_message(
        text = message,
        chat_id = chat_id
    )
    await bot.close()
    
@celery.task
def send_habit(chat_id: int, habit_title: str):
    asyncio.run(send_message_for_user_in_tg(
        message = f'Напоминаем про привыку под названием: {habit_title}',
        chat_id = chat_id
    ))
    

@celery.task
def send(chat_id: int, habit_title: str, send_time: str, days: list):
    now_day = datetime.now(pytz.timezone('Europe/Minsk')).strftime('%A').lower()
    now_time = datetime.now(pytz.timezone('Europe/Minsk')).strftime('%H:%M')
    if now_day in days and now_time == send_time:
        send_habit.apply_async(args = [chat_id, habit_title])
    
    else:
        send.apply_async(
        args = [chat_id, habit_title, send_time, days],
        eta = datetime.now(pytz.timezone('Europe/Minsk')) + timedelta(minutes = 1)
    )


def schedule_send_habit(chat_id: int, habit_title: str, send_time: str, days: list):     
    send.apply_async(
        args = [chat_id, habit_title, send_time, days],
        eta = datetime.now(pytz.timezone('Europe/Minsk')) + timedelta(minutes = 1)
    )
    

def start_sending_all_habits(habits: list['HabitModel']):
    for habit in habits: 
        schedule_send_habit(
            chat_id = habit.user.telegram_id,
            habit_title = habit.title,
            send_time = habit.time.strftime('%H:%M'),
            days = [DaysEnum(day).value for day in habit.days]
        )
    



# celery -A tasks.tasks worker --loglevel=INFO