from .. import db

from flask import request
from flask.views import MethodView


class ItemAPI(MethodView):
    init_every_request = False

    def __init__(self, model, filter_field):
        self.model = model
        self.filter_field = filter_field

    def _get_item(self, field_value):
        return self.model.query.filter(
            getattr(self.model, self.filter_field) == field_value
        ).first()

    def get(self, field_value):
        item = self._get_item(field_value)
        return item.to_dict() if item else []

    def delete(self, field_value):
        item = self._get_item(field_value)
        db.session.delete(item)
        db.session.commit()
        return "", 200


class ListAPI(MethodView):
    init_every_request = False

    def __init__(self, model, filter_field):
        self.model = model
        self.filter_field = filter_field

    def _get_item(self, field_value):
        return self.model.query.filter(
            getattr(self.model, self.filter_field) == field_value
        )

    def get(self):
        items = self.model.query.all()
        return [item.to_dict() for item in items]

    def post(self):

        data = request.json

        field_value = data.get("field_value")
        if field_value:
            item = self._get_item(field_value)

            if item:
                return "Already exists!", 400

        db.session.add(self.model(**data))
        db.session.commit()
        return "", 200


def register_api(app, model, name, filter_field="id"):
    item = ItemAPI.as_view(f"{name}-item", model, filter_field)
    group = ListAPI.as_view(f"{name}-list", model, filter_field)
    app.add_url_rule(f"/{name}/<int:field_value>", view_func=item)
    app.add_url_rule(f"/{name}/", view_func=group)
