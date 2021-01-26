from flask_sqlalchemy import SQLAlchemy
from Models.exchange import Exchange
from Models.user import User
from flask import Flask
from config import db

class User_Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchange.id'), nullable=False)

    def __init__(self, user_id, exchange_id, id=None):
        if id != None:
            self.id = id
        self.user_id = user_id
        self.exchange_id = exchange_id

    # Gets dict with the Role object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'id user': self.user_id,
            'id exchange': self.exchange_id
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}