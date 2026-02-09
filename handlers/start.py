from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers.survey import show_q1

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Здравствуйте! Я ваш виртуальный помощник. "
        "Ответы на наши вопросы помогут нам более глубоко подготовиться "
        "к разговору с Вами. Это займет совсем немного времени.\n\n"
        "Начнем"
    )
    await show_q1(message, state)
