from config import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Models.product import Product
from Models.product_sale import Product_Sale

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delete = db.Column(db.Boolean, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    lot_number = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.DateTime(), nullable=False)
    sales_number = db.Column(db.Integer, nullable=False)

    def __init__(self, month, year, lot_number, expiration_date, sales_number, delete=False, id=None):
        if id != None:
            self.id = id
        self.delete = delete
        self.month = month
        self.year = year
        self.lot_number = lot_number
        self.expiration_date = expiration_date
        self.sales_number = sales_number

    # Gets dict with the Sale Object
    @property
    def serialize(self):
        product_sale = Product_Sale.query.filter_by(sale_id = self.id).first()
        product = Product.query.filter_by(id = product_sale.product_id).first()
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'month': self.month,
            'year': self.year,
            'lot number': self.lot_number,
            'expiration date': self.expiration_date,
            'sale number': self.sales_number,
            'product': {
                'codebar': product.codebar,
                'name': product.name
            }
        }

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}