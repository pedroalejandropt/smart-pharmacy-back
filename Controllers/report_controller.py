from flask import Flask, Blueprint, jsonify, request, abort
from Errors.errors import bad_request, not_found
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from Security.jwt import token_required
import Services.report_service as report_service

api_report = Blueprint('reports', 'reports')

# Report Routes
@api_report.route('/api/v1/reports/best-sellers', methods=['POST'])
@token_required
def api_best_sellers(current_user):
    body = request.json
    sells = report_service.best_sellers(body['month'], body['year'])
    return jsonify(sells)

@api_report.route('/api/v1/reports/worst-sellers', methods=['POST'])
@token_required
def api_worst_sellers(current_user):
    body = request.json
    sells = report_service.worst_sellers(body['month'], body['year'])
    return jsonify(sells[::-1])

@api_report.route('/api/v1/reports/best-amounts', methods=['POST'])
def api_best_amounts():
    body = request.json
    sells = report_service.best_amounts(body['month'], body['year'])
    return jsonify(sells)

@api_report.route('/api/v1/reports/worst-amounts', methods=['POST'])
@token_required
def api_worst_amounts(current_user):
    body = request.json
    sells = report_service.worst_amounts(body['month'], body['year'])
    return jsonify(sells)

### Predictions

@api_report.route('/api/v1/reports/predict-best-sellers', methods=['POST'])
@token_required
def api_predict_best_sellers(current_user):
    body = request.json
    sells = report_service.predict_best_sellers(body['month'], body['year'])
    return jsonify(sells)

@api_report.route('/api/v1/reports/predict-worst-sellers', methods=['POST'])
@token_required
def api_predict_worst_sellers(current_user):
    body = request.json
    sells = report_service.predict_worst_sellers(body['month'], body['year'])
    return jsonify(sells[::-1])

@api_report.route('/api/v1/reports/predict-best-amounts', methods=['POST'])
@token_required
def api_predict_best_amounts(current_user):
    body = request.json
    sells = report_service.predict_best_amounts(body['month'], body['year'])
    return jsonify(sells)

@api_report.route('/api/v1/reports/predict-worst-amounts', methods=['POST'])
@token_required
def api_predict_worst_amounts(current_user):
    body = request.json
    sells = report_service.predict_worst_amounts(body['month'], body['year'])
    return jsonify(sells)

@api_report.route('/api/v1/reports/product-variation', methods=['POST'])
@token_required
def api_product_variation(current_user):
    body = request.json
    report = report_service.product_sell_variation(body['code'], body['year'])
    return jsonify(report)

@api_report.route('/api/v1/reports/product-variation-four', methods=['POST'])
@token_required
def api_product_variation_four(current_user):
    body = request.json
    report = report_service.product_sell_variation_four(body['code'])
    return jsonify(report)

@api_report.route('/api/v1/reports/predict-product-variation', methods=['POST'])
@token_required
def api_predict_product_variation(current_user):
    body = request.json
    report = report_service.predict_product_sell_variation(body['code'], body['year'])
    return jsonify(report)