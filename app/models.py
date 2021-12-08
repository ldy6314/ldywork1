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
    pass
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), )
    # username, password_hash, permission
