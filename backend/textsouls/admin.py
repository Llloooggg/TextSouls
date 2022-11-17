from flask import Blueprint
from flask_admin.contrib.sqla import ModelView

from . import admin
from textsouls.models import db
from textsouls.models import User

ts_admin = Blueprint("ts_admin", __name__)

admin.add_view(ModelView(User, db.session))
