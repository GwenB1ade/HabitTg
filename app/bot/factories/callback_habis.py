from aiogram.filters.callback_data import CallbackData
from typing import Optional

class CallbackViewHabitFactory(CallbackData, prefix = 'habit'):
    # Action: next, prev, habit
    action: str
    id_habit: Optional[int | str]
    value: Optional[int]