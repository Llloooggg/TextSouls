import datetime
from random import randint

from sqlalchemy.orm import backref
from sqlalchemy_serializer import SerializerMixin

from textsouls import db

from textsouls.characters.models import Character


class DuelParticipant(db.Model, SerializerMixin):

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
        return f"{self.duel_id}: {self.participant_id}"


class Duel(db.Model, SerializerMixin):

    __tablename__ = "duels"

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now()
    )
    participants = db.relationship(
        "DuelParticipant",
        backref=backref("duel", order_by="DuelParticipant.turn_order.asc()"),
        lazy="dynamic",
    )

    def attack(self, attacked_character, defensive_character):
        defensive_character_endurance = (
            defensive_character.endurance_base
            - attacked_character.battle_stats["attack_power"]
        )

        return defensive_character_endurance

    def defence(self, defensive_character):
        procced = False
        if (
            randint(
                int(10 * defensive_character.battle_stats["defence_chance"]),
                50,
            )
            == 50
        ):
            procced is True

        return procced

    def dodge(self, defensive_character):
        procced = False
        if (
            randint(
                int(10 * defensive_character.battle_stats["dodge_chance"]), 50
            )
            == 50
        ):
            procced is True

        return procced

    def duel_one_to_one(self):

        character_first = Character.query.get(
            self.participants[0].participant_id
        )
        character_second = Character.query.get(
            self.participants[1].participant_id
        )

        while (
            character_first.endurance_base > 0
            and character_second.endurance_base > 0
        ):
            if not self.defence(character_second) or not self.dodge(
                character_second
            ):
                character_second.endurance_base = self.attack(
                    character_first, character_second
                )
            if not self.defence(character_first) or not self.dodge(
                character_first
            ):
                character_first.endurance_base = self.attack(
                    character_second, character_first
                )
        if character_first.endurance_base > 0:
            return character_first.name
        elif character_second.endurance_base > 0:
            return character_second.name
        else:
            return "Ничья"
