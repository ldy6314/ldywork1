from extensions import db
from flask_login import UserMixin


class Subject(db.Model):
    pass
    # id, time, name
    # 反向引用students


class Student(db.Model):
    pass
    # id, class_name
    # 反向引用subjects


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    # username, password_hash, permission
    class_id = db.Column(db.Integer, default=0)
    permission = db.Column(db.Integer, defalut=1)
