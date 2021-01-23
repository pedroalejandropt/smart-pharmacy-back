from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delete = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(200), nullable=False)

    def __init__(self, name, delete=False, id=None):
        if id != None:
            self.id = id
        self.delete = delete
        self.name = name

    # Gets dict with the Category object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

