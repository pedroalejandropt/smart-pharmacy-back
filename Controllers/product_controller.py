from flask import Flask, Blueprint, jsonify, request, abort
import Services.product_service as product_service
from Errors.errors import bad_request, not_found
from werkzeug.exceptions import HTTPException
from Models.user_product import User_Product
from flask_sqlalchemy import SQLAlchemy
from Security.jwt import token_required
from Models.product import Product

api_product = Blueprint('products', 'products')

# Product Routes
@api_product.route('/api/v1/products', methods=['GET'])
@token_required
def api_get(current_user):
    ''' Get all entities'''
    products = product_service.get()
    return jsonify([product.as_dict() for product in products])

@api_product.route('/api/v1/products/<id>', methods=['GET'])
@token_required
def api_get_by_id(current_user, id=0):
    ''' Get all entities'''
    product = product_service.get_by_id(id)
    return jsonify(product.serialize)

@api_product.route('/api/v1/products/barcode/<id>', methods=['GET'])
@token_required
def api_get_by_barcode(current_user, id=0):
    ''' Get all entities'''
    product = product_service.get_by_barcode(id)
    return jsonify(product.serialize)

@api_product.route('/api/v1/products', methods=['POST'])
def api_post():
    ''' Create entity'''
    if not request.is_json or 'product' not in request.get_json() or 'user' not in request.get_json():
        return bad_request('Missing required data.')
    else:
        data = request.json
        product = data['product']
        user_product = data['user']
        if 'code' not in product or 'codebar' not in product or \
            'name' not in product or 'price' not in product or \
                'freeze' not in product or 'tax' not in product or \
                    'recipe' not in product or 'regulated' not in product or \
                        'rating' not in product or 'replacementClassification' not in product or \
                          'labProviderName' not in product or 'subcategory_id' not in product:
                          return bad_request('Missing required data.')
        if 'user_id' not in user_product:
            return bad_request('Missing required data.')
    print(data['product'])
    product = product_service.post(product, user_product)
    return jsonify(product.serialize)

@api_product.route('/api/v1/products/<id>', methods=['PUT'])
@token_required
def api_put(current_user, id=0):
    ''' Update entity by id'''
    body = request.json
    body['id'] = int(id)
    res = product_service.put(body)
    return jsonify(res.as_dict()) if isinstance(res, Product) else jsonify(res)

@api_product.route('/api/v1/products/<id>', methods=['DELETE'])
@token_required
def api_delete(current_user, id=0):
    ''' Delete entity by id'''
    res = product_service.delete(id)
    return jsonify(res.as_dict())
