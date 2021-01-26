from config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delete = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)

    def __init__(self, date, amount, delete=False, id=None):
        if id != None:
            self.id = id
        self.delete = delete
        self.date = date
        self.amount = amount

    # Gets dict with the Exchange Object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'date': self.date,
            'amount': self.amount
        }

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}