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
    print(type(request))
    if not request.is_json or 'email' not in request.get_json() or 'password' not in request.get_json() or 'device' not in request.get_json():
        return bad_request('Missing required data.')
    
    user = User.query.filter_by(email = request.json['email']).first()

    if not user: 
        return not_found('Correo Electrónico o Contraseña Incorrectos!')
    
    if (user.role_id == 3) and ('web' == request.json['device']):
        return bad_request('Los Empleados comunes no pueden ingresar al sistema web!')

    if user.password == request.json['password']:
        token = generate_token(user.email)
        return jsonify({'user': user.serialize,'token' : token.decode('UTF-8')})
    else:
        return bad_request('Correo Electrónico o Contraseña Incorrectos!')

@api_user.route('/api/v1/renew', methods =['POST']) 
def renew_token(): 
    if not request.is_json or 'email' not in request.get_json():
        return bad_request('Missing required data.')
    token = generate_token(request.json['email'])
    return jsonify({'token' : token.decode('UTF-8')})

