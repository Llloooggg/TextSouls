import datetime

from sqlalchemy_serializer import SerializerMixin

from textsouls import db


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
    destinations = db.relationship(
        "SendlistDestination", backref="sendlist", lazy="dynamic"
    )

    def __str__(self):
        return f"{self.id}: {self.username}"


class Sendlist(db.Model, SerializerMixin):

    __tablename__ = "sendlists"

    serialize_rules = ("-destination",)

    id = db.Column(db.BigInteger, primary_key=True)
    message = db.Column(db.String(255), nullable=True)
    destinations = db.relationship(
        "SendlistDestination", backref="sendlist", lazy="dynamic"
    )

    def __str__(self):
        return f"{self.message[:12]}..."


class SendlistDestinationStatus(db.Model, SerializerMixin):

    __tablename__ = "sendlists_destionations_statuses"

    serialize_rules = ("-destination",)

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    destinations = db.relationship(
        "SendlistDestination",
        backref="status",
        lazy="dynamic",
    )

    def __str__(self):
        return self.name


class SendlistDestination(db.Model, SerializerMixin):

    __tablename__ = "sendlists_destionations"

    id = db.Column(db.BigInteger, primary_key=True)
    sendlist_id = db.Column(
        db.Integer,
        db.ForeignKey("sendlists.id", ondelete="CASCADE"),
    )
    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id", ondelete="CASCADE"),
    )
    status_id = db.Column(
        db.Integer,
        db.ForeignKey("sendlists_destionations_types.id", ondelete="CASCADE"),
    )

    def __str__(self):
        return f"{self.message[:12]}..."
