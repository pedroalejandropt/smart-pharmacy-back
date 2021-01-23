from Models.category import Category
from Models.subcategory import Subcategory
from config import db
""" from werkzeug.exceptions import NotFound """

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return Category.query.filter_by(delete = False)

def get_subcategories(id):
    '''
    Get all entities
    :returns: all entity
    '''
    return Subcategory.query.filter_by(category_id = id)

def post(body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    category = Category(**body)
    db.session.add(category)
    db.session.commit()
    return category

def put(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    category = Category.query.get(body['id'])

    if category:
        category = Category(**body)
        db.session.merge(category)
        db.session.flush()
        db.session.commit()
        return category
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete(id):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    category = Category.query.get(id)
    
    if category:
        category.delete = True
        db.session.merge(category)
        db.session.flush()
        db.session.commit()
        return category
    raise NotFound('no such entity found with id=' + str(id))