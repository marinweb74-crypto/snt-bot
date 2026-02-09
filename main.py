import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from db import create_pool, close_pool, create_tables
from storage import PgStorage, create_fsm_table
from handlers import start, survey, post, fallback

logging.basicConfig(level=logging.INFO)


async def main():
    await create_pool()
    await create_tables()
    await create_fsm_table()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=PgStorage())

    dp.include_router(start.router)
    dp.include_router(survey.router)
    dp.include_router(post.router)
    dp.include_router(fallback.router)  # must be last — catches unhandled messages

    try:
        await dp.start_polling(bot)
    finally:
        await close_pool()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
