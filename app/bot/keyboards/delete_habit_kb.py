from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..factories.callback_del_habit import DeleteHabitFactory

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import HabitModel


def delete_habit_keyboard(list_habits: list['HabitModel'], skip_number: int = 0):
    keyboard = InlineKeyboardBuilder()
    for habit in list_habits:
        keyboard.add(InlineKeyboardButton(
            text=habit.title,
            callback_data=DeleteHabitFactory(action='habit', id_habit=str(habit.uuid), value=None).pack()
        ))
    
    keyboard.adjust(1)

    
    keyboard._markup.append([
        InlineKeyboardButton(
            text='<', callback_data=DeleteHabitFactory(action='prev', id_habit=None, value=skip_number-5).pack()
        ),
        InlineKeyboardButton(
            text=str(skip_number), callback_data='None'
        ),
        InlineKeyboardButton(
            text='>', callback_data=DeleteHabitFactory(action='next', id_habit=None, value=skip_number+5).pack()
        )
    ])

    return keyboard.as_markup()
