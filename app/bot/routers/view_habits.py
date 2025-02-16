from aiogram import Router, F
from aiogram.types import CallbackQuery

from .. import keyboards
from ..keyboards.view_habits_kb import habits_list_keyboard
from ..keyboards.base.back_kb import back_keyboard
from ..factories.callback_habis import CallbackViewHabitFactory
from service.habit_service import HabitService
from models.habit import DaysEnum

router = Router()
view_habit_callback = 'view_habits'



@router.callback_query(F.data == view_habit_callback)
async def view_habit(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    habits = HabitService.get_habits(
        telegram_id = telegram_id,
    )
    
    if habits == []:
        return await callback.message.edit_text(
            text = 'У вас еще нет привычек!',
            reply_markup = back_keyboard(back_to_callback = 'start')
        )
    
    await callback.message.edit_text(
        text = 'Вот привычки',
        reply_markup = back_keyboard(back_to_callback = 'start', keyboard = habits_list_keyboard(habits))
    )
    

@router.callback_query(CallbackViewHabitFactory.filter())
async def callback_view_habit(callback: CallbackQuery, callback_data: CallbackViewHabitFactory):
    action = callback_data.action
    telegram_id = callback.from_user.id
    keyboard = callback.message.reply_markup
    
    if action == 'prev' or action == 'next':
        skip = callback_data.value
        if skip < 0:
            skip = 0
            return None
            
        habits = HabitService.get_habits(
            telegram_id = telegram_id,
            skip = skip
        )
        
        
        if len(habits) == 0 or habits == []:
            return await callback.message.edit_text(
                text = f'Это последняя страница. Пропущенно {skip} привычек',
                reply_markup = keyboard
            )
            
        
        
        return await callback.message.edit_text(
            text = f'Вот еще (пропущенно {skip} привычек)',
            reply_markup = back_keyboard(back_to_callback = 'start', keyboard = habits_list_keyboard(habits, skip))
        )
        
        
    
    elif action == 'habit':
        habit_id = callback_data.id_habit
        habit = HabitService.get_one_habit(habit_id)
        
        days = {
            DaysEnum.Monday: 'Понедельник',
            DaysEnum.Tuesday: 'Вторник',
            DaysEnum.Wednesday: 'Среда',
            DaysEnum.Thursday: 'Четверг',
            DaysEnum.Friday: 'Пятница',
            DaysEnum.Saturday: 'Суббота',
            DaysEnum.Sunday: 'Воскресенье'
        }
        
        text = f"""Название привычки {habit.title}\nВремя оповещения: {habit.time}\nДни оповещения: {[days.get(x) for x in habit.days]}"""
        
        return await callback.message.edit_text(
            text = text,
            reply_markup = back_keyboard(back_to_callback = view_habit_callback)
        )