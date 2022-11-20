from flask import Blueprint

from textsouls.common.views import register_api
from textsouls.models import User

from textsouls.models import CharacterRace
from textsouls.models import CharacterClass
from textsouls.models import CharacterState
from textsouls.models import Character

from textsouls.models import DuelParticipant
from textsouls.models import Duel

main = Blueprint("main", __name__)

register_api(main, User, "users")

register_api(main, CharacterRace, "character_races")
register_api(main, CharacterClass, "character_classes")
register_api(main, CharacterState, "character_states")
register_api(main, Character, "characters", "owner")


register_api(main, DuelParticipant, "duels_participant")
register_api(main, Duel, "duels")
