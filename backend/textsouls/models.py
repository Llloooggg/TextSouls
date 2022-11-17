import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(
        self,
        tg_id,
        first_name,
        last_name,
        username,
        is_admin=False,
    ):
        self.tg_id = tg_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.registered_on = datetime.datetime.now()
        self.is_admin = is_admin
