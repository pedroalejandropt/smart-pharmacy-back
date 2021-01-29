from Models.exchange import Exchange
from Models.user_exchange import User_Exchange
from config import db
from werkzeug.exceptions import NotFound

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return Exchange.query.filter_by(delete = False)

def get_by_id(id):
    '''
    Get entitiy
    :returns: entity
    '''
    return Exchange.query.filter_by(id=id).first()

def post(body, user_body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    exchange = Exchange(**body)
    db.session.add(exchange)
    db.session.commit()

    user_body['exchange_id'] = exchange.id

    user_exchange = User_Exchange(**user_body)
    db.session.add(user_exchange)
    db.session.commit()
    return exchange

def put(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    exchange = Exchange.query.get(body['id'])

    if exchange:
        exchange = Exchange(**body)
        db.session.merge(exchange)
        db.session.flush()
        db.session.commit()
        return exchange
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete(id):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    exchange = Exchange.query.get(id)
    
    if exchange:
        exchange.delete = True
        db.session.merge(exchange)
        db.session.flush()
        db.session.commit()
        return exchange
    raise NotFound('no such entity found with id=' + str(id))