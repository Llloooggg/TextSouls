from flask import Blueprint
from flask import request

from . import db
from textsouls.models import User

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return "Nice!", 200


@main.route("/registration", methods=["POST"])
def registration():
    data = request.get_json()

    tg_id = data.get("tg_id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    username = data.get("username")

    existed_user = User.query.filter_by(tg_id=tg_id).first()

    if not existed_user:
        new_user = User(
            tg_id=tg_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )

        db.session.add(new_user)
        db.session.commit()

        return {"created": True, "id": new_user.id}

    else:
        return {"created": False, "id": existed_user.id}
