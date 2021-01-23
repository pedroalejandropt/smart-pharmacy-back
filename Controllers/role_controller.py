from flask import Flask, Blueprint, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from Models.role import Role
import Services.role_service as role_service
from werkzeug.exceptions import HTTPException

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

def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response

def not_found(message):
    response = jsonify({'error': message})
    response.status_code = 404
    return response