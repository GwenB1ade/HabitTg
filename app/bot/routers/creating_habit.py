from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext 
from datetime import datetime

import re

from service.habit_service import HabitService

from .. import keyboards

from ..keyboards.creating_habit_kb import days_choises_keyboard, user_selections, days_of_week
from ..factories.callback_days import CallbackDaysFactory
from tasks.tasks import schedule_send_habit

router = Router()

class CreateHabitState(StatesGroup):
    set_title_for_habit = State()
    set_time = State()
    set_days = State()

@router.callback_query(F.data == 'create_habit')
async def create_habit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text = 'Итак, для начала назовите свою привычку (максимум 50 символов)'
    )
    
    await state.set_state(CreateHabitState.set_title_for_habit)
    

@router.message(CreateHabitState.set_title_for_habit)
async def set_title_for_habit(message: Message, state: FSMContext):
    if len(message.text) > 50:
        await message.answer('Название слишком большое, максимум символов 50')
        return None
    
    await state.update_data(title = message.text)
    await state.set_state(CreateHabitState.set_time)
    await message.answer('Отлично, теперь укажи время, в которое буду я тебя оповещать. (Пример: "11:00")')
    

@router.message(CreateHabitState.set_time)
async def set_time(message: Message, state: FSMContext):
    time = message.text
    await state.update_data(time = time)
    
    pattern = r'^\d{2}:\d{2}$'
    match = re.match(pattern, time)
    if bool(match):
        await message.answer(
            text = 'Отлично, теперь укажите дни, в которые мы будем вас оповещать',
            reply_markup = days_choises_keyboard(message.from_user.id)
        )
        await state.set_state(CreateHabitState.set_days)
    
    else:
        await message.answer('Неверный формат времени, отправте еще раз (Пример: "23:00")')
        

@router.callback_query(CreateHabitState.set_days, CallbackDaysFactory.filter())
async def days_choises(callback: CallbackQuery, callback_data: CallbackDaysFactory, state: FSMContext):
   
    telegram_id = str(callback.from_user.id)
    day = callback_data.value
    if not user_selections.get(telegram_id, None):
        user_selections.update({telegram_id: {}})
    
    # if callback_data.action == 'confirm':
    #     days = []
    #     for key, value in user_selections[telegram_id].items():
    #         if value == 'tick':
    #             days.append(key)
                  
    #     await callback.message.answer('Привычка успешно создана')  
    #     data = await state.get_data()
    #     title = data['title']
    #     time = data['time']
    #     print(f'Название: {title} \n Время: {time} \n Дни: {days}')
        
        # habit = HabitService.create_habit(
        #     telegram_id = int(telegram_id),
        #     title = title,
        #     time = time,
        #     days = days
        # )
        
        # user_selections[telegram_id] = {}
        
        # return None
        
    current_selection = user_selections[telegram_id].get(day, '')

    if current_selection == '' or current_selection == 'cross':
        user_selections[telegram_id][day] = 'tick'
    elif current_selection == 'tick':
        user_selections[telegram_id][day] = 'cross'
    
    await state.update_data(telegram_id = telegram_id)
    await callback.message.edit_reply_markup(
        inline_message_id = callback.inline_message_id,
        reply_markup = days_choises_keyboard(telegram_id)
    )

@router.callback_query(F.data == 'confirm')
async def confirm(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        title = data['title']
        time = data['time']
        telegram_id = data['telegram_id']
        days = []
        
        for key, value in user_selections[telegram_id].items():
            if value == 'tick':
                days.append(key)
        print(days)
        habit = HabitService.create_habit(
            telegram_id = int(telegram_id),
            title = title,
            time = time,
            days = days
        )
        
        user_selections[telegram_id] = {}
        
        await callback.message.answer('Привычка успешно создана!')
        
        schedule_send_habit(
            chat_id = callback.message.chat.id,
            habit_title = habit.title,
            send_time = time,
            days = days
        )
    
    
