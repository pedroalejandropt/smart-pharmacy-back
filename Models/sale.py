from config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delete = db.Column(db.Boolean, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    lotNumber = db.Column(db.Integer, nullable=False)
    expirationDate = db.Column(db.DateTime(), nullable=False)
    salesNumber = db.Column(db.Integer, nullable=False)

    def __init__(self, month, year, lotNumber, expirationDate, salesNumber, delete=False, id=None):
        if id != None:
            self.id = id
        self.delete = delete
        self.month = month
        self.year = year
        self.lotNumber = lotNumber
        self.expirationDate = expirationDate
        self.salesNumber = salesNumber

    # Gets dict with the Sale Object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'month': self.month,
            'year': self.year,
            'lot number': self.lotNumber,
            'expiration date': self.expirationDate,
            'sale number': self.salesNumber
        }

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}