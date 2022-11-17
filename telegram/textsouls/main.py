import json

from aiogram import Bot, Dispatcher, executor

with open("telegram/config.json") as config_file:
    config_data = json.load(config_file)

API_TOKEN = config_data["main_settings"]["BOT_TOKEN"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message):
    await message.reply("Nice!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
