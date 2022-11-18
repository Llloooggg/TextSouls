import json

from aiogram import Bot, Dispatcher, executor

from common import backend

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)

API_TOKEN = config_data["MAIN_SETTINGS"]["BOT_TOKEN"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message):
    tg_user = message.from_user
    ts_user = {
        "id": tg_user.id,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "username": tg_user.username,
    }
    result = backend.post("/users", ts_user)
    if not result["error"]:
        response_code = result["response"].status_code
        if response_code == 200:
            await message.reply("Добро пожаловать!")
        elif response_code == 400:
            await message.reply("Добро пожаловать! Снова")
        else:
            await message.reply("Что-то другое")
    else:
        await message.reply("Упс! Что-то пошло не так")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
