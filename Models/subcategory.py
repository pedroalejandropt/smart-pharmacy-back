from flask import Flask
from flask_sqlalchemy import *
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
            'category': category.name,
            'category_id': self.category_id
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

def insert_initial_values(*args, **kwargs):
    db.session.add(Category(name='Medicamentos'))
    db.session.add(Category(name='Miscelaneos'))
    db.session.add(Category(name='Higiene Personal'))
    db.session.add(Category(name='Maquillaje'))
    db.session.commit()
    db.session.add(Subcategory(name='Malestar General', category_id=1))
    db.session.add(Subcategory(name='Antialergicos', category_id=1))
    db.session.add(Subcategory(name='Antiespasmodicos', category_id=1))
    db.session.add(Subcategory(name='Antigripales', category_id=1))
    db.session.add(Subcategory(name='Analgesicos', category_id=1))
    db.session.add(Subcategory(name='Antibióticos', category_id=1))
    db.session.add(Subcategory(name='Antiflatulentos', category_id=1))
    db.session.add(Subcategory(name='Laxantes', category_id=1))
    db.session.add(Subcategory(name='Digestivos', category_id=1))
    db.session.add(Subcategory(name='Psicotrópicos', category_id=1))
    db.session.add(Subcategory(name='Bebidas', category_id=2))
    db.session.add(Subcategory(name='Alimentos Dulces', category_id=2))
    db.session.add(Subcategory(name='Alimentos Salados', category_id=2))
    db.session.add(Subcategory(name='Shampoo', category_id=3))
    db.session.add(Subcategory(name='Jabón en Barra', category_id=3))
    db.session.add(Subcategory(name='Jabón Líquido', category_id=3))
    db.session.add(Subcategory(name='Papel Higiénico', category_id=3))
    db.session.add(Subcategory(name='Pintura de Uñas', category_id=4))
    db.session.add(Subcategory(name='Base', category_id=4))
    db.session.add(Subcategory(name='Mascara de Pestañas', category_id=4))
    db.session.add(Subcategory(name='Pintura de Labios', category_id=4))
    db.session.add(Subcategory(name='Corrector', category_id=4))
    db.session.commit()

event.listen(Subcategory.__table__, 'after_create', insert_initial_values)