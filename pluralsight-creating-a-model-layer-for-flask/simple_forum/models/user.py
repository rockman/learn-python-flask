
from simple_forum.db import db
from simple_forum.login import login_manager

from flask_login import UserMixin

from uuid import uuid4


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    uuid = db.Column(db.String(64), nullable=False, default=lambda: str(uuid4()))

    def get_id(self):
        return self.uuid


@login_manager.user_loader
def load_user(user_uuid):
    return User.query.filter_by(uuid=user_uuid).first()