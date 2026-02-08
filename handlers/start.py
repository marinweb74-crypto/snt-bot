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
        "Здравствуйте! Это бот для подачи информации о задолженностях в СНТ.\n\n"
        "Вам будет предложено ответить на 10 вопросов.\n"
        "Начнём!"
    )
    await show_q1(message, state)
