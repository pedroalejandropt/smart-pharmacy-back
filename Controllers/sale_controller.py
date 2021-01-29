from flask import Flask, Blueprint, jsonify, request, abort
import Services.sale_service as sale_service
from Errors.errors import bad_request, not_found
from werkzeug.exceptions import HTTPException
from Models.product_sale import Product_Sale
from flask_sqlalchemy import SQLAlchemy
from Security.jwt import token_required
from Models.sale import Sale

api_sale = Blueprint('sales', 'sales')

# Sale Routes
@api_sale.route('/api/v1/sales', methods=['GET'])
@token_required
def api_get(current_user):
    ''' Get all entities'''
    sales = sale_service.get()
    return jsonify([sale.as_dict() for sale in sales])

@api_sale.route('/api/v1/sales/<id>', methods=['GET'])
@token_required
def api_get_by_id(current_user, id=0):
    ''' Get all entities'''
    sale = sale_service.get_by_id(id)
    return jsonify(sale.serialize)

@api_sale.route('/api/v1/sales', methods=['POST'])
def api_post():
    ''' Create entity'''
    if not request.is_json or 'sale' not in request.get_json() or 'product' not in request.get_json():
        return bad_request('Missing required data.')
    else:
        data = request.json
        sale = data['sale']
        product_sale = data['product']
        if 'month' not in sale or 'year' not in sale or \
            'lotNumber' not in sale or 'expirationDate' not in sale or \
                'salesNumber' not in sale:
                return bad_request('Missing required data.')
        if 'product_id' not in product_sale:
            return bad_request('Missing required data.')
    sale = sale_service.post(sale, product_sale)
    return jsonify(sale.serialize)

@api_sale.route('/api/v1/sales/<id>', methods=['PUT'])
@token_required
def api_put(current_user, id=0):
    ''' Update entity by id'''
    body = request.json
    body['id'] = int(id)
    res = sale_service.put(body)
    return jsonify(res.as_dict()) if isinstance(res, Sale) else jsonify(res)

@api_sale.route('/api/v1/sales/<id>', methods=['DELETE'])
@token_required
def api_delete(current_user, id=0):
    ''' Delete entity by id'''
    res = sale_service.delete(id)
    return jsonify(res.as_dict())
