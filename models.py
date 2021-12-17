from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    password_hash = db.Column(db.String(128))
    # username, password_hash, permission
    class_id = db.Column(db.Integer)
    name = db.Column(db.String(10))
    permission = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    students = db.relationship('Student', backref='class')


association_table = db.Table(
    'association',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    name = db.Column(db.String(20))
    contact1 = db.Column(db.String(20))
    contact2 = db.Column(db.String(20))
    subjects = db.relationship(
        'Subject',
        secondary=association_table,
        back_populates='students'
    )


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    time = db.Column(db.String(50))
    price = db.Column(db.Integer)
    canceled = db.Column(db.Integer)
    remark = db.Column(db.Text)
    students = db.relationship(
        'Student',
        secondary=association_table,
        back_populates='subjects'
    )

