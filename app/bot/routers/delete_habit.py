from aiogram import Router, F
from aiogram.types import CallbackQuery

from .. import keyboards
from ..keyboards.base.back_kb import back_keyboard
from ..keyboards.delete_habit_kb import delete_habit_keyboard
from ..factories.callback_del_habit import DeleteHabitFactory

from service.habit_service import HabitService

router = Router()
    
    
@router.callback_query(F.data == 'remove_habit')
async def remove_habit(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    habits = HabitService.get_habits(
        telegram_id = telegram_id,
    )
    
    if habits == []:
        return await callback.message.edit_text(
            text = 'У вас нету ни одной заметки!',
            reply_markup = back_keyboard(back_to_callback = 'start')
        )
    
    await callback.message.edit_text(
        text = 'Выберите привычку для удаления',
        reply_markup = delete_habit_keyboard(habits)
    )
    

@router.callback_query(DeleteHabitFactory.filter())
async def remove_habit_filter(callback: CallbackQuery, callback_data: DeleteHabitFactory):
    action = callback_data.action
    telegram_id = callback.from_user.id
    
    if action == 'prev' or action == 'next':
        skip = callback_data.value
        habits = HabitService.get_habits(
            telegram_id = telegram_id,
            skip = skip
        )
        
        return await callback.message.edit_text(
            text = f'Выберите привычку для удаления. Пропущенно {skip} привычек',
            reply_markup = delete_habit_keyboard(habits, skip_number = skip)
        )
    
    elif action == 'habit':
        habit_id = callback_data.id_habit
        habit = HabitService.delete_habit(
            habit_id = habit_id
        )
        habits = HabitService.get_habits(
            telegram_id = telegram_id,
        )
        
        return await callback.message.edit_text(
            text = f'Привычка под названием: "{habit.title}" была удалена',
            reply_markup = delete_habit_keyboard(habits)
        )
    
    
