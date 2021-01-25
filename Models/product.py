from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db
from Models.subcategory import Subcategory
from Models.category import Category

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delete = db.Column(db.Boolean, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    codebar = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    freeze = db.Column(db.Integer, nullable=False)
    tax = db.Column(db.Integer, nullable=False)
    recipe = db.Column(db.Integer, nullable=False)
    regulated = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    replacementClassification = db.Column(db.Integer, nullable=False)
    labProviderName = db.Column(db.String(200), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)

    def __init__(self, code, codebar, name, price, freeze, tax, recipe, regulated, rating, replacementClassification, labProviderName, subcategory_id, delete=False, id=None):
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
        self.replacementClassification = replacementClassification
        self.labProviderName = labProviderName
        self.subcategory_id = subcategory_id

    # Gets dict with the Product object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        subcategory = Subcategory.query.filter_by(id = self.subcategory_id).first()
        category = Category.query.filter_by(id = subcategory.category_id).first()
        return {
            'id': self.id,
            'code': self.code,
            'codebar': self.codebar,
            'name': self.name,
            'price': self.price,
            'freeze': self.freeze,
            'tax': self.tax,
            'recipe': self.recipe,
            'regulated': self.regulated,
            'rating': self.rating,
            'replacementClassification': self.replacementClassification,
            'labProviderName': self.labProviderName,
            'category': category.name,
            'subcategory': subcategory.name
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

