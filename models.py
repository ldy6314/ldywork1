from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    # username, password_hash, permission
    class_id = db.Column(db.Integer)
    name = db.Column(db.String(10))
    permission = db.Column(db.Integer)

