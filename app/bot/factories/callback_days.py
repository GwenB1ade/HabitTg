from typing import Optional
from aiogram.filters.callback_data import CallbackData

class CallbackDaysFactory(CallbackData, prefix = 'day'):
    action: str
    value: Optional[str]
    