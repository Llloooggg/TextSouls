from flask import Blueprint

from textsouls import admin

from textsouls.common.database import db
from textsouls.common.api import register_api
from textsouls.common.admin import CommonAdminView

from textsouls.actions.models import DuelParticipant
from textsouls.actions.models import Duel


actions_bp = Blueprint("actions", __name__)

register_api(actions_bp, DuelParticipant, "duels_participant")
register_api(actions_bp, Duel, "duels")

admin.add_view(CommonAdminView(DuelParticipant, db.session))
admin.add_view(CommonAdminView(Duel, db.session))
