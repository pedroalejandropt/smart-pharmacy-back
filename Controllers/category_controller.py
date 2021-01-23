from flask import Flask, Blueprint, jsonify, request, abort
import Services.category_service as category_service
from Errors.errors import bad_request, not_found
from werkzeug.exceptions import HTTPException
from Models.subcategory import Subcategory
from Security.jwt import token_required
from flask_sqlalchemy import SQLAlchemy
from Models.category import Category

api_category = Blueprint('categories', 'categories')

# Category Routes
@api_category.route('/api/v1/categories', methods=['GET'])
@token_required
def api_get(current_user):
    ''' Get all entities'''
    categories = category_service.get()
    return jsonify([category.as_dict() for category in categories])

@api_category.route('/api/v1/categories/<id>/subcategories', methods=['GET'])
@token_required
def api_get_subcategories_by_category(current_user, id=0):
    ''' Get all entities'''
    if id == 0:
        return bad_request('Missing required data.')

    category = Category.query.filter_by(id = id).first()

    if category == None:
        return bad_request('Category do not exist.')

    subcategories = category_service.get_subcategories(id)
    return jsonify([subcategory.serialize for subcategory in subcategories])

@api_category.route('/api/v1/categories', methods=['POST'])
@token_required
def api_post(current_user):
    ''' Create entity'''
    if not request.is_json or 'name' not in request.get_json():
        return bad_request('Missing required data.')

    category = category_service.post(request.json)
    return jsonify(category.serialize)

@api_category.route('/api/v1/categories/<id>', methods=['PUT'])
@token_required
def api_put(current_user, id=0):
    ''' Update entity by id'''
    body = request.json
    body['id'] = int(id)
    print(body)
    res = category_service.put(body)
    return jsonify(res.as_dict()) if isinstance(res, Category) else jsonify(res)

@api_category.route('/api/v1/categories/<id>', methods=['DELETE'])
@token_required
def api_delete(current_user, id=0):
    ''' Delete entity by id'''
    res = category_service.delete(id)
    return jsonify(res.as_dict())

