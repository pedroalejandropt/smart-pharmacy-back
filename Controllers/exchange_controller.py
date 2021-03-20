from flask import Flask, Blueprint, jsonify, request, abort
import Services.exchange_service as exchange_service
from Errors.errors import bad_request, not_found
from werkzeug.exceptions import HTTPException
from Models.user_exchange import User_Exchange
from flask_sqlalchemy import SQLAlchemy
from Security.jwt import token_required
from Models.exchange import Exchange

api_exchange = Blueprint('exchanges', 'exchanges')

# Exchange Routes
@api_exchange.route('/api/v1/exchanges', methods=['GET'])
@token_required
def api_get(current_user):
    ''' Get all entities'''
    exchanges = exchange_service.get()
    return jsonify([exchange.serialize for exchange in exchanges])

@api_exchange.route('/api/v1/exchanges/<id>', methods=['GET'])
@token_required
def api_get_by_id(current_user, id=0):
    ''' Get all entities'''
    exchange = exchange_service.get_by_id(id)
    return jsonify(exchange.serialize)

@api_exchange.route('/api/v1/exchanges', methods=['POST'])
def api_post():
    ''' Create entity'''
    if not request.is_json or 'exchange' not in request.get_json() or 'user' not in request.get_json():
        return bad_request('Missing required data.')
    else:
        data = request.json
        exchange = data['exchange']
        user_exchange = data['user']
        if 'date' not in exchange or 'amount' not in exchange:
            return bad_request('Missing required data.')
        if 'user_id' not in user_exchange:
            return bad_request('Missing required data.')
    exchange = exchange_service.post(exchange, user_exchange)
    return jsonify(exchange.serialize)

@api_exchange.route('/api/v1/exchanges/<id>', methods=['PUT'])
@token_required
def api_put(current_user, id=0):
    ''' Update entity by id'''
    body = request.json
    body['id'] = int(id)
    res = exchange_service.put(body)
    return jsonify(res.as_dict()) if isinstance(res, Exchange) else jsonify(res)

@api_exchange.route('/api/v1/exchanges/<id>', methods=['DELETE'])
@token_required
def api_delete(current_user, id=0):
    ''' Delete entity by id'''
    res = exchange_service.delete(id)
    return jsonify(res.as_dict())
