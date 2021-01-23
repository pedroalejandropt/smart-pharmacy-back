from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db
from Models.category import Category

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delete = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __init__(self, name, category_id, delete=False, id=None):
        if id != None:
            self.id = id
        self.delete = delete
        self.name = name
        self.category_id = category_id

    # Gets dict with the Subcategory object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        category = Category.query.filter_by(id = self.category_id).first()
        return {
            'id': self.id,
            'name': self.name,
            'category': category.name
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

