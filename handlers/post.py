from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import NOTIFY_CHAT_ID

router = Router()

BOT_USERNAME = "testanket222_bot"


@router.message(Command("post"))
async def cmd_post(message: Message):
    text = (
        "Уважаемые председатели СНТ!\n\n"
        "Если в вашем товариществе есть должники, "
        "наши специалисты готовы помочь вам в решении этого вопроса.\n\n"
        "Заполните короткую анкету — это займёт всего пару минут. "
        "После этого мы свяжемся с вами для консультации."
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Заполнить анкету",
            url=f"https://t.me/{BOT_USERNAME}?start=true",
        )],
    ])

    await message.bot.send_message(
        chat_id=NOTIFY_CHAT_ID,
        text=text,
        reply_markup=keyboard,
    )
    await message.answer("Пост с кнопкой отправлен в канал!")
