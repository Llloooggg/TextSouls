from flask import Blueprint

from flask_admin.contrib.sqla import ModelView

from textsouls import db
from textsouls import admin

from textsouls.common.api import register_api

from textsouls.users.models import User


class UserAdminView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        self.form_columns = self.column_list
        super(UserAdminView, self).__init__(model, *args, **kwargs)


bp = Blueprint("users", __name__)

register_api(bp, User, "users")

admin.add_view(UserAdminView(User, db.session))
