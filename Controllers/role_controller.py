from flask import Flask, Blueprint, jsonify, request, abort
from Errors.errors import bad_request, not_found
from werkzeug.exceptions import HTTPException
import Services.role_service as role_service
from flask_sqlalchemy import SQLAlchemy
from Security.jwt import token_required
from Models.role import Role

api_role = Blueprint('roles', 'roles')

# Role Routes
@api_role.route('/api/v1/roles', methods=['GET'])
def api_get():
    ''' Get all entities'''
    roles = role_service.get()
    return jsonify([role.as_dict() for role in roles])

@api_role.route('/api/v1/roles', methods=['POST'])
def api_post():
    ''' Create entity'''
    if not request.is_json or 'name' not in request.get_json():
        return bad_request('Missing required data.')

    role = role_service.post(request.json)
    return jsonify(role.serialize)

@api_role.route('/api/v1/roles/<id>', methods=['PUT'])
@token_required
def api_put(current_user, id=0):
    ''' Update entity by id'''
    body = request.json
    body['id'] = int(id)
    print(body)
    res = role_service.put(body)
    return jsonify(res.as_dict()) if isinstance(res, Role) else jsonify(res)

@api_role.route('/api/v1/roles/<id>', methods=['DELETE'])
@token_required
def api_delete(current_user, id=0):
    ''' Delete entity by id'''
    res = role_service.delete(id)
    return jsonify(res.as_dict())
