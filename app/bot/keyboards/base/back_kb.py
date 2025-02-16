from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_keyboard(
    back_to_callback: str,
    keyboard: InlineKeyboardMarkup = None
    ) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой назад. Если передать keyboard, то к этой клавиатуре добавиться кнопка 'Назад'
    """
    
    if keyboard is None: 
        keyboard = InlineKeyboardBuilder(markup = [
            [
                InlineKeyboardButton(text = 'Назад', callback_data = back_to_callback)
            ]
        ])
        
        return keyboard.as_markup()
    
    else:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text = 'Назад', callback_data = back_to_callback)
        ])
        
        return keyboard

