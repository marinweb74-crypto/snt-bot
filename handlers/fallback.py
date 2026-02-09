from aiogram import Router
from aiogram.types import Message, CallbackQuery

router = Router()


@router.message()
async def fallback_message(message: Message):
    """Catch any message that didn't match a state handler."""
    await message.answer(
        "Для начала анкеты нажмите /start"
    )


@router.callback_query()
async def fallback_callback(callback: CallbackQuery):
    """Catch any stale inline button press."""
    await callback.answer(
        "Эта кнопка устарела. Нажмите /start чтобы начать заново.",
        show_alert=True,
    )
