import json

from flask import Flask
from flask_migrate import Migrate


from textsouls.common.database import db
from textsouls.common.admin import admin

from textsouls.actions.api import actions_bp
from textsouls.characters.api import characters_bp
from textsouls.users.api import users_bp


app = Flask(
    "__name__",
)

migrate = Migrate(app, db, compare_type=True)

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)

main_settings = config_data["MAIN_SETTINGS"]
app.config.update(main_settings)

db_settings = config_data["DB_SETTINGS"]
app.config.update(db_settings)

celery_settings = config_data["CELERY_SETTINGS"]
app.config.update(celery_settings)

db.init_app(app)
admin.init_app(app)

app.register_blueprint(actions_bp)
app.register_blueprint(characters_bp)
app.register_blueprint(users_bp)
