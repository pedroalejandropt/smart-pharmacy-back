from Models.role import Role
from config import db
""" from werkzeug.exceptions import NotFound """

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return Role.query.filter_by(delete = False)

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

def put(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    role = Role.query.get(body['id'])

    if role:
        role = Role(**body)
        db.session.merge(role)
        db.session.flush()
        db.session.commit()
        return role
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete(id):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    role = Role.query.get(id)
    
    if role:
        role.delete = True
        db.session.merge(role)
        db.session.flush()
        db.session.commit()
        return role
    raise NotFound('no such entity found with id=' + str(id))