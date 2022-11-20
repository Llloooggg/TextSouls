import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(
    "__name__",
)
db = SQLAlchemy()

migrate = Migrate(app, db, compare_type=True)
admin = Admin(name="TextSouls")

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)

main_settings = config_data["MAIN_SETTINGS"]
app.config.update(main_settings)

db_settings = config_data["DB_SETTINGS"]
app.config.update(db_settings)

admin.init_app(app)
db.init_app(app)

from textsouls.actions.api import bp

app.register_blueprint(bp)

from textsouls.characters.api import bp

app.register_blueprint(bp)

from textsouls.users.api import bp

app.register_blueprint(bp)
