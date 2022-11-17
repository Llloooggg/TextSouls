import json

from aiogram import Bot, Dispatcher, executor

from common import backend

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)

API_TOKEN = config_data["main_settings"]["bot_token"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message):
    tg_user = message.from_user
    ts_user = {
        "tg_id": tg_user.id,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "username": tg_user.username,
    }
    backend.post("/registration", ts_user)
    await message.reply("Nice!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
