from typing import Optional
from aiogram.filters.callback_data import CallbackData

class DeleteHabitFactory(CallbackData, prefix = 'delete_habit'):
    # action: prev, next, habit
    action: str
    value: Optional[int]
    id_habit: Optional[int | str]