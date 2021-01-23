from Models.user import User
from config import db
""" from werkzeug.exceptions import NotFound """

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return User.query.filter_by(delete = False)

def get_by_id(id):
    '''
    Get entitiy
    :returns: entity
    '''
    return User.query.filter_by(id=id).first()

def post(body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    user = User(**body)
    db.session.add(user)
    db.session.commit()
    return user

def put(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    user = User.query.get(body['id'])

    if user:
        user = User(**body)
        db.session.merge(user)
        db.session.flush()
        db.session.commit()
        return user
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete(id):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    user = User.query.get(id)
    
    if user:
        user.delete = True
        db.session.merge(user)
        db.session.flush()
        db.session.commit()
        return user
    raise NotFound('no such entity found with id=' + str(id))