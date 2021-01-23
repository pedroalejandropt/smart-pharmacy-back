from Models.role import Role
from config import db
""" from werkzeug.exceptions import NotFound """

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return Role.query.all()

def post(body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    role = Role(**body)
    db.session.add(role)
    db.session.commit()
    return role