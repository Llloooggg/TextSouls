from flask import Blueprint
from flask_admin.contrib.sqla import ModelView

from . import admin
from textsouls.models import db

from textsouls.models import User

from textsouls.models import CharacterRace
from textsouls.models import CharacterClass
from textsouls.models import CharacterState
from textsouls.models import Character

from textsouls.models import DuelParticipants
from textsouls.models import Duel

ts_admin = Blueprint("ts_admin", __name__)


class AdminView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        self.form_columns = self.column_list
        super(AdminView, self).__init__(model, *args, **kwargs)


class CommonView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        super(CommonView, self).__init__(model, *args, **kwargs)


admin.add_view(AdminView(User, db.session))

admin.add_view(CommonView(CharacterRace, db.session))
admin.add_view(CommonView(CharacterClass, db.session))
admin.add_view(CommonView(CharacterState, db.session))
admin.add_view(CommonView(Character, db.session))

admin.add_view(CommonView(DuelParticipants, db.session))
admin.add_view(CommonView(Duel, db.session))
