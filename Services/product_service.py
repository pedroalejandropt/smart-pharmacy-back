from Models.product import Product
from config import db
""" from werkzeug.exceptions import NotFound """

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return Product.query.all()

def post(body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    product = Product(**body)
    db.session.add(product)
    db.session.commit()
    return product