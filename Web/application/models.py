from application import db
import datetime as dt
from flask_login import UserMixin

class Entry(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String, nullable=False)
    prediction = db.Column(db.String, nullable=False)
    predicted_on = db.Column(db.DateTime, nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String,  nullable=False)
    entries = db.relationship('Entry', backref='user', lazy=True)