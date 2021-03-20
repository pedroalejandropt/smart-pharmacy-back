from flask import Flask, Blueprint, jsonify, request, abort
import Services.product_service as product_service
from Errors.errors import bad_request, not_found
from Services.ml_service import predict, train
from werkzeug.exceptions import HTTPException
from Models.product_sale import Product_Sale
import Services.sale_service as sale_service
from flask_sqlalchemy import SQLAlchemy
from Security.jwt import token_required
from Models.product import Product
from Models.sale import Sale
import csv

api_sale = Blueprint('sales', 'sales')

# Sale Routes
@api_sale.route('/api/v1/sales', methods=['GET'])
@token_required
def api_get(current_user):
    ''' Get all entities'''
    sales = sale_service.get()
    return jsonify([sale.serialize for sale in sales])

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

@api_sale.route('/api/v1/sales/upload', methods=['POST'])
@token_required
def api_upload(current_user):
    file = request.files['file']
    fstring = file.read().decode("latin-1")
    #fstring = file.read().splitlines()
    #lines = [line.decode("utf-8", errors="ignore") for line in fstring]
    csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]

    for i in csv_dicts:
        verify = False
        product = product_service.get_by_barcode(i["ï»¿codebar"])
        if (product is None):
            verify = True
            product = { 'code': i['code'], 'codebar': i['ï»¿codebar'], 'name': i['name'], 'price': i['price'], 'freeze': i['freeze'], 'tax': i['tax'], 'recipe': i['recipe'], 'regulated': i['regulated'], 'rating': i['rating'], 'replacementClassification': i['replacementClassification'], 'labProviderName': i['labProviderName'], 'subcategory_id': i['subcategory_id'] }
            sale = { 'month': i['month'], 'year': i['year'], 'lotNumber': i['lotNumber'], 'expirationDate': i['expirationDate'], 'salesNumber': i['salesNumber'] }
            user = { 'user_id': 1 }
            product_added = product_service.post(product, user)
            product_sale = { 'product_id': product_added.id }
            sale_added = sale_service.post(sale, product_sale)
            print('producto/venta agregado')
        else:
            sale = { 'month': i['month'], 'year': i['year'], 'lotNumber': i['lotNumber'], 'expirationDate': i['expirationDate'], 'salesNumber': i['salesNumber'] }
            product_sale = { 'product_id': product.id }
            sale_added = sale_service.post(sale, product_sale)
            print('producto existe / Venta Agregada')
        if verify:
            train(i['year'], i['month'], product_added, sale_added)
        else:
            train(i['year'], i['month'], product, sale_added)
    response="Whatever you wish too return"
    return jsonify(response)
