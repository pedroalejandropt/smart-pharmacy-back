from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from setup.db import db

class Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)

    def __init__(self, name):
        self.name = name

    # Gets dict with the Exchange Object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'date': self.date,
            'amount': self.amount
        }