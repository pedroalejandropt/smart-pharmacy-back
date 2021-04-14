from Models.parameter import Parameter
from Models.user_parameter import User_Parameter
from config import db
""" from werkzeug.exceptions import NotFound """

def get():
    '''
    Get all entities
    :returns: all entity
    '''
    return Parameter.query.filter_by(delete = False)

def post(body):
    '''
    Create entity with body
    :param body: request body
    :returns: the created entity
    '''
    parameter = Parameter(**body)
    db.session.add(parameter)
    db.session.commit()

    user_parameter_body = {'user_id': 1, 'parameter_id': parameter.id}

    user_parameter = User_Parameter(**user_parameter_body)
    db.session.add(user_parameter)
    db.session.commit()

    return parameter

def put(body):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    parameter = Parameter.query.get(body['id'])

    if parameter:
        parameter = Parameter(**body)
        db.session.merge(parameter)
        db.session.flush()
        db.session.commit()
        return parameter
    raise NotFound('no such entity found with id=' + str(body['id']))

def delete(id):
    '''
    Update entity by id
    :param body: request body
    :returns: the updated entity
    '''
    parameter = Parameter.query.get(id)
    
    if parameter:
        parameter.delete = True
        db.session.merge(parameter)
        db.session.flush()
        db.session.commit()
        return parameter
    raise NotFound('no such entity found with id=' + str(id))