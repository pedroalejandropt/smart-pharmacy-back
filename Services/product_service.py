from Models.product import Product
from Models.user_product import User_Product
from config import db
from werkzeug.exceptions import NotFound

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return Product.query.filter_by(delete = False)

def get_by_barcode(id):
    '''
    Get entitiy
    :returns: entity
    '''
    return Product.query.filter_by(codebar=id).first()

def get_by_id(id):
    '''
    Get entitiy
    :returns: entity
    '''
    return Product.query.filter_by(id=id).first()

def post(body, user_body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    product = Product(**body)
    db.session.add(product)
    db.session.commit()

    user_body['product_id'] = product.id

    user_product = User_Product(**user_body)
    db.session.add(user_product)
    db.session.commit()
    return product

def put(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    product = Product.query.get(body['id'])

    if product:
        product = Product(**body)
        db.session.merge(product)
        db.session.flush()
        db.session.commit()
        return product
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete(id):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    product = Product.query.get(id)
    
    if product:
        product.delete = True
        db.session.merge(product)
        db.session.flush()
        db.session.commit()
        return product
    raise NotFound('no such entity found with id=' + str(id))