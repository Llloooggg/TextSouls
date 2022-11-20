from flask import Blueprint

from textsouls import db
from textsouls import admin

from textsouls.common.api import register_api
from textsouls.common.api import CommonAdminView

from textsouls.actions.models import DuelParticipant
from textsouls.actions.models import Duel


bp = Blueprint("actions", __name__)

register_api(bp, DuelParticipant, "duels_participant")
register_api(bp, Duel, "duels")

admin.add_view(CommonAdminView(DuelParticipant, db.session))
admin.add_view(CommonAdminView(Duel, db.session))
