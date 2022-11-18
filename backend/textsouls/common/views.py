from .. import db

from flask import request
from flask import jsonify
from flask.views import MethodView


class ItemAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model

    def _get_item(self, id):
        return self.model.query.get_or_404(id)

    def get(self, id):
        item = self._get_item(id)
        return item.to_dict()

    def delete(self, id):
        item = self._get_item(id)
        db.session.delete(item)
        db.session.commit()
        return "", 200


class ListAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model

    def _get_item(self, id):
        return self.model.query.filter_by(id=id).first()

    def get(self):
        items = self.model.query.all()
        return jsonify([item.to_dict() for item in items])

    def post(self):

        data = request.json

        if data.get("id"):
            item = self._get_item(data["id"])

            if item:
                return "Already exists!", 400

        db.session.add(self.model(**data))
        db.session.commit()
        return "", 200


def register_api(app, model, name):
    item = ItemAPI.as_view(f"{name}-item", model)
    group = ListAPI.as_view(f"{name}-list", model)
    app.add_url_rule(f"/{name}/<int:id>", view_func=item)
    app.add_url_rule(f"/{name}/", view_func=group)
