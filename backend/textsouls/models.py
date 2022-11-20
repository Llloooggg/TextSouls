import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()


class User(db.Model, SerializerMixin):

    __tablename__ = "users"

    serialize_rules = ("-character",)

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    chat_id = db.Column(db.BigInteger, nullable=False, unique=True)
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
    endurance_koef = db.Column(db.Float(), nullable=False, unique=False)
    strength_koef = db.Column(db.Float(), nullable=False, unique=False)
    agility_koef = db.Column(db.Float(), nullable=False, unique=False)
    defence_koef = db.Column(db.Float(), nullable=False, unique=False)
    wisdom_koef = db.Column(db.Float(), nullable=False, unique=False)

    def __str__(self):
        return self.name


class CharacterClass(db.Model, SerializerMixin):

    __tablename__ = "character_classes"

    serialize_rules = ("-characters",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True, unique=True)
    characters = db.relationship("Character", backref="class", lazy="dynamic")
    endurance_koef = db.Column(db.Float(), nullable=False, unique=False)
    strength_koef = db.Column(db.Float(), nullable=False, unique=False)
    agility_koef = db.Column(db.Float(), nullable=False, unique=False)
    defence_koef = db.Column(db.Float(), nullable=False, unique=False)
    wisdom_koef = db.Column(db.Float(), nullable=False, unique=False)

    def __str__(self):
        return self.name


class CharacterState(db.Model, SerializerMixin):

    __tablename__ = "character_states"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    characters = db.relationship("Character", backref="state", lazy="dynamic")

    def __str__(self):
        return self.name


class Character(db.Model, SerializerMixin):

    __tablename__ = "characters"

    serialize_rules = ("-user", "-race", "-class")

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="CASCADE"),
    )
    name = db.Column(db.String(255), nullable=False, unique=True)
    character_race_id = db.Column(
        db.Integer,
        db.ForeignKey("character_races.id", ondelete="CASCADE"),
        nullable=False,
    )
    character_class_id = db.Column(
        db.Integer,
        db.ForeignKey("character_classes.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_on = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    endurance_base = db.Column(db.Integer(), nullable=False, unique=False)
    strength_base = db.Column(db.Integer(), nullable=False, unique=False)
    agility_base = db.Column(db.Integer(), nullable=False, unique=False)
    defence_base = db.Column(db.Integer(), nullable=False, unique=False)
    wisdom_base = db.Column(db.Integer(), nullable=False, unique=False)
    state_id = db.Column(
        db.Integer,
        db.ForeignKey("character_states.id", ondelete="CASCADE"),
        nullable=False,
        default=1,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        char_race = CharacterRace.query.get(self.character_race)
        char_class = CharacterClass.query.get(self.character_class)

        self.endurance_base = (
            100 * char_race.endurance_koef * char_class.endurance_koef
        )
        self.strength_base = (
            100 * char_race.strength_koef * char_class.strength_koef
        )
        self.agility_base = (
            100 * char_race.agility_koef * char_class.agility_koef
        )
        self.defence_base = (
            100 * char_race.defence_koef * char_class.defence_koef
        )
        self.wisdom_base = 100 * char_race.wisdom_koef * char_class.wisdom_koef

    def __str__(self):
        return self.name

    @property
    def battle_stats(self):
        char_race = CharacterRace.query.get(self.character_race)
        char_class = CharacterClass.query.get(self.character_class)

        attack_power = (
            self.strength_base
            * char_race.strength_koef
            * char_class.strength_koef
        )

        defence_chance = (
            self.defence_base
            * char_race.defence_koef
            * char_class.defence_koef
        )

        dodge_chance = (
            self.agility_base
            * char_race.agility_koef
            * char_class.agility_koef
        )

        return {
            "attack_power": attack_power,
            "defence_chance": defence_chance,
            "dodge_chance": dodge_chance,
        }


class DuelParticipants(db.Model, SerializerMixin):

    __tablename__ = "duels_participants"

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(
        db.Integer,
        db.ForeignKey("characters.id", ondelete="CASCADE"),
    )
    turn_order = db.Column(db.Integer, nullable=False)
    duel_id = db.Column(
        db.Integer,
        db.ForeignKey("duels.id", ondelete="CASCADE"),
    )

    def __str__(self):
        return self.duel_id, self.participant_id


class Duel(db.Model, SerializerMixin):

    __tablename__ = "duels"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    participants = db.relationship(
        "DuelParticipants", backref="duel", lazy="dynamic"
    )
