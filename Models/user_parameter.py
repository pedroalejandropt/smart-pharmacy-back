from flask_sqlalchemy import *
from Models.parameter import Parameter
from Models.user import User
from flask import Flask
from config import db
import threading 

class Add_Parameter():
    def __init__(self, value):
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

class User_Parameter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameter.id'), nullable=False)

    def __init__(self, user_id, parameter_id, id=None):
        if id != None:
            self.id = id
        self.user_id = user_id
        self.parameter_id = parameter_id

    # Gets dict with the Role object
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'id user': self.user_id,
            'id parameter': self.parameter_id
        }

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def cancel_schedule():
    global job
    job.cancel()
    print()

def parameter_schedule(min):
    global job
    global add
    add.set_value(True)
    """ print('Start') """
    job = threading.Timer(min * 3600, parameter_schedule, args=(min,))
    job.start()

def insert_initial_values(*args, **kwargs):
    db.session.add(Parameter(frecuency=0, value=4))
    db.session.commit()
    db.session.add(User_Parameter(user_id=1, parameter_id=1))
    db.session.commit()
    parameter_schedule(1)

event.listen(User_Parameter.__table__, 'after_create', insert_initial_values)

add = Add_Parameter(False)
parameter_schedule(4)
job = 0