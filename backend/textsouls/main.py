from flask import Blueprint

from textsouls.common.views import register_api
from textsouls.models import User

from textsouls.models import CharacterRace
from textsouls.models import CharacterClass
from textsouls.models import Character

main = Blueprint("main", __name__)

register_api(main, User, "users")

register_api(main, CharacterRace, "character_races")
register_api(main, CharacterClass, "character_classes")
register_api(main, Character, "characters", "owner")
