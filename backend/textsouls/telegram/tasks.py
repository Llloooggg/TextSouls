from textsouls.common.database import db
from textsouls import celery

from textsouls.users.models import User, Sendlist, SendlistDestination


@celery.task()
def broadcast_message(message):
    sendlist = Sendlist(message=message)
    db.session.add(sendlist)
    db.session.commit()
    for user in User.query.all():
        db.session.add(
            SendlistDestination(sendlist_id=sendlist.id, user_id=user.id)
        )
    db.session.commit()
