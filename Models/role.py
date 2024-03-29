from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

    # Gets dict with the Role object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}