from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..factories.callback_habis import CallbackViewHabitFactory

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.habit import HabitModel




def habits_list_keyboard(list_habits: list['HabitModel'], skip_number: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for habit in list_habits:
        keyboard.add(InlineKeyboardButton(
            text=habit.title,
            callback_data=CallbackViewHabitFactory(action='habit', id_habit=str(habit.uuid), value=None).pack()
        ))
    
    keyboard.adjust(1)

    
    keyboard._markup.append([
        InlineKeyboardButton(
            text='<', callback_data=CallbackViewHabitFactory(action='prev', id_habit=None, value=skip_number-5).pack()
        ),
        InlineKeyboardButton(
            text=str(skip_number), callback_data='None'
        ),
        InlineKeyboardButton(
            text='>', callback_data=CallbackViewHabitFactory(action='next', id_habit=None, value=skip_number+5).pack()
        )
    ])

    return keyboard.as_markup()
