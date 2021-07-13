from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db
from Models.subcategory import Subcategory
from Models.category import Category

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delete = db.Column(db.Boolean, nullable=False)
    code = db.Column(db.Numeric(100), nullable=False)
    codebar = db.Column(db.Numeric(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    freeze = db.Column(db.Integer, nullable=False)
    tax = db.Column(db.Integer, nullable=False)
    recipe = db.Column(db.Integer, nullable=False)
    regulated = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    replacement_classification = db.Column(db.String(100), nullable=False)
    lab_provider_name = db.Column(db.String(200), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)

    def __init__(self, code, codebar, name, price, freeze, tax, recipe, regulated, rating, replacement_classification, lab_provider_name, subcategory_id, delete=False, id=None):
        if id != None:
            self.id = id
        self.delete = delete
        self.code = code
        self.codebar = codebar
        self.name = name
        self.price = price
        self.freeze = freeze
        self.tax = tax
        self.recipe = recipe
        self.regulated = regulated
        self.rating = rating
        self.replacement_classification = replacement_classification
        self.lab_provider_name = lab_provider_name
        self.subcategory_id = subcategory_id

    # Gets dict with the Product object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        subcategory = Subcategory.query.filter_by(id = self.subcategory_id).first()
        category = Category.query.filter_by(id = subcategory.category_id).first()
        return {
            'id': str(self.id),
            'code': str(self.code),
            'codebar': str(self.codebar),
            'name': str(self.name),
            'price': str(self.price),
            'freeze': self.freeze,
            'tax': self.tax,
            'recipe': self.recipe,
            'regulated': self.regulated,
            'rating': str(self.rating),
            'replacement_classification': str(self.replacement_classification),
            'lab_provider_name': str(self.lab_provider_name),
            'subcategory_id': str(self.subcategory_id)
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

