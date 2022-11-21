from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class CommonAdminView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        super(CommonAdminView, self).__init__(model, *args, **kwargs)


admin = Admin(name="TextSouls")
