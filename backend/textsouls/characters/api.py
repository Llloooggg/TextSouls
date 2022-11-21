from flask import Blueprint

from textsouls.common.database import db
from textsouls.common.admin import admin

from textsouls.common.api import register_api
from textsouls.common.admin import CommonAdminView

from textsouls.characters.models import CharacterRace
from textsouls.characters.models import CharacterClass
from textsouls.characters.models import CharacterState
from textsouls.characters.models import Character


bp = Blueprint("characters", __name__)

register_api(bp, CharacterRace, "character_races")
register_api(bp, CharacterClass, "character_classes")
register_api(bp, CharacterState, "character_states")
register_api(bp, Character, "characters", "owner")

admin.add_view(CommonAdminView(CharacterRace, db.session))
admin.add_view(CommonAdminView(CharacterClass, db.session))
admin.add_view(CommonAdminView(CharacterState, db.session))
admin.add_view(CommonAdminView(Character, db.session))


from textsouls.telegram.tasks import broadcast_message


@bp.route("/test", methods=["POST"])
def run_task():
    task = broadcast_message.delay()
    return str(task.id), 202
