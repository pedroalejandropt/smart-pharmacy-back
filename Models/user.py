from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import db
from Models.role import Role

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delete = db.Column(db.Boolean, nullable=False)
    identificationNumber = db.Column(db.Integer, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    secondLastName = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    phoneNumber = db.Column(db.String(50), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def __init__(self, identificationNumber, firstName, middleName, lastName, email, password, role_id, phoneNumber=None, secondLastName=None, delete=False, id=None):
        if id != None:
            self.id = id
        self.delete = delete
        self.identificationNumber = identificationNumber
        self.firstName = firstName
        self.middleName = middleName
        self.lastName = lastName
        self.secondLastName = secondLastName
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber
        self.role_id = role_id

    # Gets dict with the User object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        role = Role.query.filter_by(id = self.role_id).first()
        return {
            'id': self.id,
            'identification': self.identificationNumber,
            'firstName': self.firstName,
            'middleName': self.middleName,
            'lastName': self.lastName,
            'secondLastName': self.secondLastName,
            'email': self.email,
            'password': self.password,
            'phoneNumber': self.phoneNumber,
            'role': role.name
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

