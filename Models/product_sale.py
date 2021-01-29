from flask_sqlalchemy import SQLAlchemy
from Models.product import Product
from Models.sale import Sale
from flask import Flask
from config import db

class Product_Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)

    def __init__(self, product_id, sale_id, id=None):
        if id != None:
            self.id = id
        self.product_id = product_id
        self.sale_id = sale_id

    # Gets dict with the Product_Sale object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'id product': self.product_id,
            'id sale': self.sale_id
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}