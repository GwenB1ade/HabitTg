from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard = InlineKeyboardBuilder(markup = [
    [
        InlineKeyboardButton(text = 'Создать привычку', callback_data = 'create_habit'),
        InlineKeyboardButton(text = 'Посмотреть привычки', callback_data = 'view_habits'),
        InlineKeyboardButton(text = 'Удалить привычку', callback_data = 'remove_habit')
    ]
])