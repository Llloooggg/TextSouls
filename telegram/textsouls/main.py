import json

from fastapi import FastAPI

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)

app = FastAPI()

bot = Bot(token=config_data["MAIN_SETTINGS"]["BOT_TOKEN"])
dp = Dispatcher(storage=MemoryStorage())


@app.get("/")
async def root():
    return {"message": "Hello World"}
