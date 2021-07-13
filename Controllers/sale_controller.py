from flask import Flask, Blueprint, jsonify, request, abort
import Services.product_service as product_service
from Errors.errors import bad_request, not_found
from Services.ml_service import train_from_file
from werkzeug.exceptions import HTTPException
from Models.product_sale import Product_Sale
import Services.sale_service as sale_service
from flask_sqlalchemy import SQLAlchemy
from Security.jwt import token_required
from Models.product import Product
from Models.sale import Sale
import pandas as pd
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
            'lot_number' not in sale or 'expiration_date' not in sale or \
                'sales_number' not in sale:
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
    filetype = ("xls" in file.filename)
    try:
        df = pd.read_excel(file) if (filetype) else pd.read_csv(file, encoding = "latin")
        for index, row in df.iterrows():
            verify = False
            product = product_service.get_by_barcode(row["CODIGO BARRAS"])
            if (product is None):
                verify = True
                product = { 'code': row['CODIGO'], 'codebar': row['CODIGO BARRAS'], 'name': row['PRODUCTO'], 'price': row['NUEVO PRECIO'], 'freeze': row['REFRIGERADO'], 'tax': row['IMPUESTO'], 'recipe': row['RECIPE'], 'regulated': row['REGULADO.1'], 'rating': row['VALORACION'], 'replacement_classification': row['CLA. ABC'], 'lab_provider_name': row['NOMBRE LABORATORIO'], 'subcategory_id': row['SUBCATE'] }
                sale = { 'month': row['MES'], 'year': row['YEAR'], 'lot_number': row['NUM LOTE'], 'expiration_date': row['FECHA VENCIMIENTO'], 'sales_number': row['VENTA'] }
                user = { 'user_id': 1 }
                product_added = product_service.post(product, user)
                product_sale = { 'product_id': product_added.id }
                sale_added = sale_service.post(sale, product_sale)
                print('Producto/Venta Agregados')
            else:
                sale = { 'month': row['MES'], 'year': row['YEAR'], 'lot_number': row['NUM LOTE'], 'expiration_date': row['FECHA VENCIMIENTO'], 'sales_number': row['VENTA'] }
                product_sale = { 'product_id': product.id }
                sale_added = sale_service.post(sale, product_sale)
                print('Producto Existente / Venta Agregada')
            if verify:
                train_from_file(row['YEAR'], row['MES'], product_added, sale_added)
            else:
                train_from_file(row['YEAR'], row['MES'], product, sale_added)
        res = "Completo el Proceso ETL"
        return jsonify({'code': 200, 'msg': res})
    except:
        res = "Error en el Proceso ETL"
        return jsonify({'code': 400, 'msg': res})
