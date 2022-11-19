import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()


class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    serialize_rules = ("-character",)

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    characters = db.relationship("Character", backref="user", lazy="dynamic")

    def __str__(self):
        return f"{self.id}: {self.username}"


class CharacterRace(db.Model, SerializerMixin):

    __tablename__ = "character_races"

    serialize_rules = ("-characters",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True, unique=True)
    characters = db.relationship("Character", backref="race", lazy="dynamic")
    endurance_koef = db.Column(db.Float(), nullable=True, unique=False)
    strength_koef = db.Column(db.Float(), nullable=True, unique=False)
    agility_koef = db.Column(db.Float(), nullable=True, unique=False)
    defence_koef = db.Column(db.Float(), nullable=True, unique=False)
    wisdom_koef = db.Column(db.Float(), nullable=True, unique=False)

    def __str__(self):
        return self.name


class CharacterClass(db.Model, SerializerMixin):

    __tablename__ = "character_classes"

    serialize_rules = ("-characters",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True, unique=True)
    characters = db.relationship("Character", backref="class", lazy="dynamic")
    endurance_koef = db.Column(db.Float(), nullable=True, unique=False)
    strength_koef = db.Column(db.Float(), nullable=True, unique=False)
    agility_koef = db.Column(db.Float(), nullable=True, unique=False)
    defence_koef = db.Column(db.Float(), nullable=True, unique=False)
    wisdom_koef = db.Column(db.Float(), nullable=True, unique=False)

    def __str__(self):
        return self.name


class Character(db.Model, SerializerMixin):

    __tablename__ = "characters"

    serialize_rules = ("-user", "-race", "-class")

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="CASCADE"),
    )
    name = db.Column(db.String(255), nullable=False, unique=True)
    character_race = db.Column(
        db.Integer,
        db.ForeignKey("character_races.id", ondelete="CASCADE"),
        nullable=False,
    )
    character_class = db.Column(
        db.Integer,
        db.ForeignKey("character_classes.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_on = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )

    endurance_base = db.Column(db.Integer(), nullable=True, unique=False)
    strength_base = db.Column(db.Integer(), nullable=True, unique=False)
    agility_base = db.Column(db.Integer(), nullable=True, unique=False)
    defence_base = db.Column(db.Integer(), nullable=True, unique=False)
    wisdom_base = db.Column(db.Integer(), nullable=True, unique=False)

    def __str__(self):
        return self.name

    @property
    def attack_power(self):
        return (
            self.strength_base
            * self.character_race.strength_koef
            * self.character_class.strength_koef
        )

    @property
    def defence_chance(self):
        return (
            self.defence_base
            * self.character_race.defence_koef
            * self.character_class.defence_koef
        )

    @property
    def saving_chance(self):
        return (
            self.agility_base
            * self.character_race.agility_koef
            * self.character_class.agility_koef
        )
