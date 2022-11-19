import json

from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin

from textsouls.models import db

app = Flask(
    "__name__",
)

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

from .admin import ts_admin as ts_admin_blueprint

app.register_blueprint(ts_admin_blueprint)

from .main import main as main_blueprint

app.register_blueprint(main_blueprint)
