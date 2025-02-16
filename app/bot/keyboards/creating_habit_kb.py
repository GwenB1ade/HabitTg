from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..factories.callback_days import CallbackDaysFactory


days_of_week = {
    'monday': 'Понедельник',
    'tuesday': 'Вторник',
    'wednesday': 'Среда',
    'thursday': 'Четверг',
    'friday': 'Пятница',
    'saturday': 'Суббота',
    'sunday': 'Воскресенье'
}

user_selections = {}


def days_choises_keyboard(telegram_id: int | str):
    telegram_id = str(telegram_id)
    keyboard = InlineKeyboardBuilder() 
    buttons = []
    for day, label in days_of_week.items():
        selection = user_selections.get(telegram_id, {}).get(day, '')
        if selection == 'tick':
            button_text = f"{label} ✅"
        elif selection == 'cross' or selection == '':
            button_text = f"{label} ❌"
        
        keyboard.button(text = button_text, callback_data = CallbackDaysFactory(action='change_day', value=day))
    
    keyboard.adjust(3)
    keyboard._markup.append([InlineKeyboardButton(text = 'Подтвердить', callback_data = 'confirm')])
    return keyboard.as_markup()
    