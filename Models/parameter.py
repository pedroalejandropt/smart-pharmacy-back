from config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Parameter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delete = db.Column(db.Boolean, nullable=False)
    frecuency = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __init__(self, frecuency, value, delete=False, id=None):
        if id != None:
            self.id = id
        self.delete = delete
        self.frecuency = frecuency
        self.value = value

    # Gets dict with the Exchange Object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'frecuency': self.frecuency,
            'value': self.value
        }

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}