from flask import Flask, Blueprint, jsonify, request, abort
import Services.subcategory_service as subcategory_service
from Errors.errors import bad_request, not_found
from werkzeug.exceptions import HTTPException
from Models.subcategory import Subcategory
from Security.jwt import token_required
from flask_sqlalchemy import SQLAlchemy
from Models.category import Category

api_subcategory = Blueprint('subcategories', 'subcategories')

# Subcategory Routes
@api_subcategory.route('/api/v1/subcategories', methods=['GET'])
@token_required
def api_get(current_user):
    ''' Get all entities'''
    subcategories = subcategory_service.get()
    return jsonify([subcategory.as_dict() for subcategory in subcategories])

@api_subcategory.route('/api/v1/subcategories', methods=['POST'])
@token_required
def api_post(current_user):
    ''' Create entity'''
    if not request.is_json or 'name' not in request.get_json() or 'category_id' not in request.get_json():
        return bad_request('Missing required data.')

    subcategory = subcategory_service.post(request.json)
    return jsonify(subcategory.serialize)

@api_subcategory.route('/api/v1/subcategories/<id>', methods=['PUT'])
@token_required
def api_put(current_user, id=0):
    ''' Update entity by id'''
    body = request.json
    body['id'] = int(id)
    print(body)
    res = subcategory_service.put(body)
    return jsonify(res.as_dict()) if isinstance(res, Subcategory) else jsonify(res)

@api_subcategory.route('/api/v1/subcategories/<id>', methods=['DELETE'])
@token_required
def api_delete(current_user, id=0):
    ''' Delete entity by id'''
    res = subcategory_service.delete(id)
    return jsonify(res.as_dict())
