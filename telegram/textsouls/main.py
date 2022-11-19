import json

from fastapi import FastAPI

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from textsouls.handlers import control
from textsouls.handlers import character_creation

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)

app = FastAPI()


async def start_bot():
    bot = Bot(token=config_data["MAIN_SETTINGS"]["BOT_TOKEN"])
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(control.router)
    dp.include_router(character_creation.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())


@app.get("/")
async def root():
    return {"message": "Hello World"}
