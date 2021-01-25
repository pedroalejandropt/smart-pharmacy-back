from flask_sqlalchemy import SQLAlchemy
from Models.product import Product
from Models.user import User
from flask import Flask
from config import db

class User_Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __init__(self, user_id, product_id, id=None):
        if id != None:
            self.id = id
        self.user_id = user_id
        self.product_id = product_id

    # Gets dict with the Role object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'id user': self.user_id,
            'id product': self.product_id
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}