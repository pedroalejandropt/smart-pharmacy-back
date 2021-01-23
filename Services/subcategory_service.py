from Models.subcategory import Subcategory
from config import db
from werkzeug.exceptions import NotFound

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return Subcategory.query.filter_by(delete = False)

def post(body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    subcategory = Subcategory(**body)
    db.session.add(subcategory)
    db.session.commit()
    return subcategory

def put(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    subcategory = Subcategory.query.get(body['id'])

    if subcategory:
        subcategory = Subcategory(**body)
        db.session.merge(subcategory)
        db.session.flush()
        db.session.commit()
        return subcategory
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete(id):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    subcategory = Subcategory.query.get(id)
    
    if subcategory:
        subcategory.delete = True
        db.session.merge(subcategory)
        db.session.flush()
        db.session.commit()
        return subcategory
    raise NotFound('no such entity found with id=' + str(id))