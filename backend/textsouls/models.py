import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()


class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    character = db.relationship("Character", backref="user", lazy="dynamic")

    def __str__(self):
        return f"{self.id}: {self.username}"


class CharacterRace(db.Model, SerializerMixin):

    __tablename__ = "character_races"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    character = db.relationship("Character", backref="race", lazy="dynamic")

    def __str__(self):
        return self.name


class CharacterClass(db.Model, SerializerMixin):

    __tablename__ = "character_classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    character = db.relationship("Character", backref="class", lazy="dynamic")

    def __str__(self):
        return self.name


class Character(db.Model, SerializerMixin):

    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    name = db.Column(db.String(255), nullable=False)
    character_race = db.Column(
        db.Integer,
        db.ForeignKey("character_races.id"),
        nullable=False,
    )
    character_class = db.Column(
        db.Integer,
        db.ForeignKey("character_classes.id"),
        nullable=False,
    )
    created_on = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )

    def __str__(self):
        return self.name
