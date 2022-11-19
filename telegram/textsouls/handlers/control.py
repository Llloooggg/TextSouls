from aiogram import Router
from aiogram.filters import Command

from textsouls.common import backend

from textsouls.handlers.character_creation import CharachterCreation
from textsouls.handlers.character_creation import character_creation


router = Router()


@router.message(Command(commands=["start"]))
async def start(message, state):

    tg_user = message.from_user
    ts_user = {
        "id": tg_user.id,
        "chat_id": message.chat.id,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "username": tg_user.username,
    }

    result = backend.post("/users", ts_user)
    if not result["error"]:
        response_code = result["response"].status_code
        if response_code == 200:
            await message.reply("Привет, скиталец!", reply_markup="")
            await state.set_state(CharachterCreation.choosing_race)
            await character_creation(message, state)
        elif response_code == 400:
            await message.reply("Добро пожаловать! Снова")
        else:
            await message.reply("Что-то случилось")
    else:
        await message.reply("Упс! Что-то пошло не так")
