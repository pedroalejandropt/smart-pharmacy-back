from Models.sale import Sale
from Models.product_sale import Product_Sale
from config import db
from werkzeug.exceptions import NotFound

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return Sale.query.filter_by(delete = False)

def get_by_id(id):
    '''
    Get entitiy
    :returns: entity
    '''
    return Sale.query.filter_by(id=id).first()

def post(body, product_body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    sale = Sale(**body)
    db.session.add(sale)
    db.session.commit()

    product_body['sale_id'] = sale.id

    product_sale = Product_Sale(**product_body)
    db.session.add(product_sale)
    db.session.commit()
    return sale

def put(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    sale = Sale.query.get(body['id'])

    if sale:
        sale = Sale(**body)
        db.session.merge(sale)
        db.session.flush()
        db.session.commit()
        return sale
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete(id):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    sale = Sale.query.get(id)
    
    if sale:
        sale.delete = True
        db.session.merge(sale)
        db.session.flush()
        db.session.commit()
        return sale
    raise NotFound('no such entity found with id=' + str(id))