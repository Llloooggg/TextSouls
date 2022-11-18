import json

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import control
from handlers import character_creation

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)


async def main():
    bot = Bot(token=config_data["MAIN_SETTINGS"]["BOT_TOKEN"])
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(control.router)
    dp.include_router(character_creation.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
