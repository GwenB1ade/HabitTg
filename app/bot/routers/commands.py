from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from ..keyboards.view_habits_kb import habits_list_keyboard
from  ..keyboards.base.back_kb import back_keyboard
from service.habit_service import HabitService
from service.user_service import UserService
from .. import keyboards

from aiogram.fsm.context import FSMContext
from .creating_habit import CreateHabitState

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    username = message.from_user.username
    telegram_id = message.from_user.id
    UserService.create_user(
        username = username,
        user_telegram_id = telegram_id
    )
    
    await message.answer(
        f'Привет {username}. Это трекер привычек. Тут ты сможешь создать привычку',
        reply_markup = keyboards.start_keyboard.as_markup()
    )
    

@router.message(Command('habitslist'))
async def habits_list(message: Message):
    telegram_id = message.from_user.id
    habits = HabitService.get_habits(
        telegram_id = telegram_id,
    )
    
    if habits == []:
        return await message.edit_text(
            text = 'У вас нету ни одной привычки!',
            reply_markup = back_keyboard('start')
        )
    
    await message.answer(
        text = 'Вот привычки',
        reply_markup = back_keyboard(
            back_to_callback = 'start',
            keyboard = habits_list_keyboard(habits)
        )
    )
    

@router.message(Command('habitcreate'))
async def habit_create(message: Message, state: FSMContext):
    await message.answer(
        text = 'Итак, для начала назовите свою привычку (максимум 50 символов)'
    )

    await state.set_state(CreateHabitState.set_title_for_habit)