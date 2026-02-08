import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from db import create_pool, close_pool, create_tables
from handlers import start, survey

logging.basicConfig(level=logging.INFO)


async def main():
    await create_pool()
    await create_tables()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(survey.router)

    try:
        await dp.start_polling(bot)
    finally:
        await close_pool()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
