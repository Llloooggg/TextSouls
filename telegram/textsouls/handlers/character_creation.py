from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State

from textsouls.common import backend
from textsouls.keyboards.common import row_kb


router = Router()

available_races = {}
available_classes = {}


class CharachterCreation(StatesGroup):
    choosing_race = State()
    choosing_class = State()
    choosing_name = State()
    creation_ending = State()


@router.message(Command(commands=["createchar"]))
async def character_creation(message, state):

    global available_races
    result = backend.get("/character_races")
    if not result["error"] and result["response"].status_code == 200:
        for race in result["response"].json():
            available_races[race["name"]] = race["id"]

    await message.answer(
        text="Выбери расу:",
        reply_markup=row_kb(available_races.keys()),
    )
    await state.set_state(CharachterCreation.choosing_class)


@router.message(CharachterCreation.choosing_class)
async def race_chosen(message, state):

    if not available_races.get(message.text):
        await message.answer(
            text="Хм, такую не знаю.\nПопробуй из вариантов ниже:",
            reply_markup=row_kb(available_races),
        )
    else:
        await state.update_data(chosen_race=message.text)

        global available_classes
        result = backend.get("/character_classes")
        if not result["error"] and result["response"].status_code == 200:
            for char_class in result["response"].json():
                available_classes[char_class["name"]] = char_class["id"]
        await message.answer(
            text="А теперь выбери класс:",
            reply_markup=row_kb(available_classes.keys()),
        )
        await state.set_state(CharachterCreation.choosing_name)


@router.message(CharachterCreation.choosing_name)
async def class_chosen(message, state):

    if not available_classes.get(message.text):
        await message.answer(
            text="Хм, такой не знаю.\nПопробуй из вариантов ниже:",
            reply_markup=row_kb(available_classes),
        )
    else:
        await state.update_data(chosen_class=message.text)

        await message.answer(
            text=f"Ну, неплохо.\nА зовут-то тебя как, {message.text.lower()}?",
            reply_markup="",
        )
        await state.set_state(CharachterCreation.creation_ending)


@router.message(CharachterCreation.creation_ending)
async def name_chosen(message, state):

    name = message.text

    user_elections = await state.get_data()

    new_character = {
        "owner": message.from_user.id,
        "name": name,
        "character_race": available_races[user_elections["chosen_race"]],
        "character_class": available_classes[user_elections["chosen_class"]],
    }

    result = backend.post("/characters", new_character)
    if not result["error"] and result["response"].status_code == 200:
        await message.answer(
            text="Так и запишем.\nТеперь постарайся не умереть",
            reply_markup="",
        )
        await state.clear()
    else:
        await message.answer(
            text="Что-то пошло не так!\nДавай-ка по-новой",
        )
        await state.set_state(CharachterCreation.choosing_race)
        await character_creation(message, state)
