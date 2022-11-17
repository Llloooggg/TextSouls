import json

from flask import Flask
from flask_migrate import Migrate

from textsouls.models import db

app = Flask(
    "__name__",
)

migrate = Migrate(app, db)

with open("textsouls/config.json") as config_file:
    config_data = json.load(config_file)

main_settings = config_data["main_settings"]
app.config.update(main_settings)

db_settings = config_data["db_settings"]
app.config.update(db_settings)

db.init_app(app)


from .main import main as main_blueprint

app.register_blueprint(main_blueprint)
