from aiogram import Router, F
from aiogram.types import CallbackQuery
from service.user_service import UserService
from .. import keyboards

router = Router()


@router.callback_query(F.data == 'start')
async def start(callback: CallbackQuery):
    username = callback.from_user.username
    telegram_id = callback.from_user.id
    UserService.create_user(
        username = username,
        user_telegram_id = telegram_id
    )
    
    await callback.message.edit_text(
        f'Привет {username}. Это трекер привычек. Тут ты сможешь создать привычку',
        reply_markup = keyboards.start_keyboard.as_markup()
    )