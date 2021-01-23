from flask import Flask, Blueprint, jsonify, request, abort
from Security.jwt import token_required, generate_token
from Errors.errors import bad_request, not_found
import Services.user_service as user_service
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from Models.user import User

api_user = Blueprint('users', 'users')

# User Routes
@api_user.route('/api/v1/users', methods=['GET'])
@token_required
def api_get(current_user):
    ''' Get all entities'''
    users = user_service.get()
    return jsonify([user.as_dict() for user in users])

@api_user.route('/api/v1/users/<id>', methods=['GET'])
@token_required
def api_get_by_id(current_user, id=0):
    ''' Get all entities'''
    user = user_service.get_by_id(id)
    return jsonify(user.serialize)

@api_user.route('/api/v1/users', methods=['POST'])
def api_post():
    ''' Create entity'''
    if not request.is_json or 'identificationNumber' not in request.get_json() or 'firstName' not in request.get_json() or 'lastName' not in request.get_json() or 'email' not in request.get_json() or 'password' not in request.get_json() or 'role_id' not in request.get_json():
        return bad_request('Missing required data.')
    user = User.query.filter(or_(User.identificationNumber == request.json['identificationNumber'], User.email == request.json['email'])).all()
    if user:
        return bad_request('User already exist.')

    user = user_service.post(request.json)
    return jsonify(user.serialize)

@api_user.route('/api/v1/users/<id>', methods=['PUT'])
@token_required
def api_put(current_user, id=0):
    ''' Update entity by id'''
    body = request.json
    body['id'] = int(id)
    print(body)
    res = user_service.put(body)
    return jsonify(res.as_dict()) if isinstance(res, User) else jsonify(res)

@api_user.route('/api/v1/users/<id>', methods=['DELETE'])
@token_required
def api_delete(current_user, id=0):
    ''' Delete entity by id'''
    res = user_service.delete(id)
    return jsonify(res.as_dict())

@api_user.route('/api/v1/login', methods =['POST']) 
def login(): 
    if not request.is_json or 'email' not in request.get_json() or 'password' not in request.get_json():
        return bad_request('Missing required data.')
    
    user = User.query.filter_by(email = request.json['email']).first()

    if not user: 
        return not_found('User does not exist')

    if user.password == request.json['password']:
        token = generate_token(user.email)
        return jsonify({'user': user.serialize,'token' : token.decode('UTF-8')})
    else:
        return bad_request('Error')

    """ if not auth or not auth.get('email') or not auth.get('password'): 
        # returns 401 if any email or / and password is missing 
        return make_response( 
            'Could not verify', 
            401, 
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'} 
        ) 
   
    user = User.query\ 
        .filter_by(email = auth.get('email'))\ 
        .first() 
   
    if not user: 
        # returns 401 if user does not exist 
        return make_response( 
            'Could not verify', 
            401, 
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'} 
        ) 
   
    if check_password_hash(user.password, auth.get('password')): 
        # generates the JWT Token 
        token = jwt.encode({ 
            'public_id': user.public_id, 
            'exp' : datetime.utcnow() + timedelta(minutes = 30) 
        }, app.config['SECRET_KEY']) 
   
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201) 
    # returns 403 if password is wrong 
    return make_response( 
        'Could not verify', 
        403, 
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'} 
    )  """
