from flask import Blueprint
from flask_admin.contrib.sqla import ModelView

from . import admin
from textsouls.models import db
from textsouls.models import User

ts_admin = Blueprint("ts_admin", __name__)


class AdminView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        self.form_columns = self.column_list
        super(AdminView, self).__init__(model, *args, **kwargs)


admin.add_view(AdminView(User, db.session))
