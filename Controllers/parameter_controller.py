from flask import Flask, Blueprint, jsonify, request, abort
from Errors.errors import bad_request, not_found
from werkzeug.exceptions import HTTPException
import Services.parameter_service as parameter_service
from flask_sqlalchemy import SQLAlchemy
from Security.jwt import token_required
from Models.parameter import Parameter
from Models.user_parameter import parameter_schedule, cancel_schedule, add

api_parameter = Blueprint('parameters', 'parameters')

# Parameter Routes
@api_parameter.route('/api/v1/parameters/exchange', methods=['GET'])
def api_get_add():
    return jsonify(add.get_value())

@api_parameter.route('/api/v1/parameters', methods=['GET'])
def api_get():
    ''' Get all entities'''
    parameters = parameter_service.get()
    return jsonify([parameter.as_dict() for parameter in parameters])

@api_parameter.route('/api/v1/parameters', methods=['POST'])
@token_required
def api_post(current_user):
    ''' Create entity'''
    if not request.is_json or 'frecuency' not in request.get_json() or 'value' not in request.get_json():
        return bad_request('Missing required data.')

    parameter = parameter_service.post(request.json)
    return jsonify(parameter.serialize)

@api_parameter.route('/api/v1/parameters/<id>', methods=['PUT'])
@token_required
def api_put(current_user, id=0):
    ''' Update entity by id'''
    body = request.json
    body['id'] = int(id)
    print(body)
    res = parameter_service.put(body)
    cancel_schedule()
    if int(body['frecuency']) == 0:
        parameter_schedule(int(body['value']))
    elif int(body['frecuency']) == 1:
        parameter_schedule(24)
    else:
        parameter_schedule(168)
    return jsonify(res.as_dict()) if isinstance(res, Parameter) else jsonify(res)

@api_parameter.route('/api/v1/parameters/<id>', methods=['DELETE'])
@token_required
def api_delete(current_user, id=0):
    ''' Delete entity by id'''
    res = parameter_service.delete(id)
    return jsonify(res.as_dict())
