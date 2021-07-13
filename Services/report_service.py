from config import db
from Models.sale import Sale
from Models.product import Product
from werkzeug.exceptions import NotFound
from Models.product_sale import Product_Sale
from Services.ml_service import *
from operator import itemgetter
from datetime import datetime

months_labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

def worst_sellers(month, year):
    sellers = []
    result = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Product.name, Sale.year, Sale.month, Sale.sales_number)
        .filter(Sale.month == month, Sale.year == year)
        .order_by(Sale.sales_number)
        .order_by(Sale.year)
        .order_by(Sale.month)
        .order_by(Product.code)
        .distinct(Sale.year, Sale.month, Product.code, Sale.sales_number)
    ).limit(10).all()
    for item in result:
        sellers.append({ "year": item.year, "month": item.month, "product": item.name.title(), "Ventas": round(item.sales_number, 0) })
    return sellers

def best_sellers(month, year):
    sellers = []
    result = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Product.name, Sale.year, Sale.month, Sale.sales_number)
        .filter(Sale.month == month, Sale.year == year)
        .order_by(Sale.sales_number.desc())
        .order_by(Sale.year)
        .order_by(Sale.month)
        .order_by(Product.code)
        .distinct(Sale.year, Sale.month, Product.code, Sale.sales_number)
    ).limit(10).all()
    for item in result:
        sellers.append({ "year": item.year, "month": item.month, "product": item.name.title(), "Ventas": round(item.sales_number) })
    return sellers

def worst_amounts(month, year):
    amounts = []
    total = 0
    result = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Product.name, Sale.year, Sale.month, Sale.sales_number, (Sale.sales_number * Product.price).label('amount'))
        .filter(Sale.month == month, Sale.year == year)
        .order_by((Sale.sales_number * Product.price))
        .order_by(Product.code)
        .order_by(Sale.year)
        .order_by(Sale.month)
        .distinct((Sale.sales_number * Product.price), Product.code)
    ).limit(10).all()
    for item in result:
        total = total + item.amount
        amounts.append({ "year": item.year, "month": item.month, "product": item.name.title(), "amount": round(item.amount , 2)})
    return {"total": total, "data": amounts}

def best_amounts(month, year):
    amounts = []
    total = 0
    result = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Product.name, Sale.year, Sale.month, Sale.sales_number, (Sale.sales_number * Product.price).label('amount'))
        .filter(Sale.month == month, Sale.year == year)
        .order_by((Sale.sales_number * Product.price).desc())
        .order_by(Product.code)
        .order_by(Sale.year)
        .order_by(Sale.month)
        .distinct((Sale.sales_number * Product.price), Product.code)
    ).limit(10).all()
    for item in result:
        total = total + item.amount
        amounts.append({ "year": item.year, "month": item.month, "product": item.name.title(), "amount": round(item.amount , 2) })
    return {"total": total, "data": amounts}

def product_sell_variation_four(code):
    report = []
    actual_year = datetime.now().year
    first_year = actual_year - 3
    for i in range(first_year, actual_year + 1):
        result = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
            .join(Product, Product_Sale.product_id == Product.id)
            .add_columns(Product.code, Product.name, Sale.year, Sale.month, Sale.sales_number)
            .filter(Sale.year == i, Product.code == code)
            .order_by(Sale.month)
            .distinct(Sale.month)
        ).all()
        if (len(result) == 0):
            report.append({"year": i, "data": [ { "month": 1, "ventas": 0 }, { "month": 2, "ventas": 0 }, { "month": 3, "ventas": 0 }, { "month": 4, "ventas": 0 }, { "month": 5, "ventas": 0 }, { "month": 6, "ventas": 0 }, { "month": 7, "ventas": 0 }, { "month": 8, "ventas": 0 }, { "month": 9, "ventas": 0 }, { "month": 10, "ventas": 0 }, { "month": 11, "ventas": 0 }, { "month": 12, "ventas": 0 } ]})
        else:  
            data = []      
            for item in result:
                data.append({ "month": item.month, "ventas": item.sales_number })
                #print(item.keys())
            report.append({"year": i, "data": data})
    return report

def product_sell_variation(code, year):
    report = []
    result = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Product.name, Sale.year, Sale.month, Sale.sales_number)
        .filter(Sale.year == year, Product.code == code)
        .order_by(Sale.month)
        .distinct(Sale.month)
    ).all()
    for item in result:
        #print(item.keys())
        report.append({ "month": months_labels[item.month - 1], "ventas": round(item.sales_number, 0) })
    return report

## Predictions

def predict_worst_sellers(month, year):
    sellers = []
    products = Product.query.filter_by(delete = False)
    for item in products:
        sellers.append({ "year": year, "month": month, "product": item.name.title(), "Ventas": round(predict(int(year), int(month), float(item.code)), 0) })
    sellers = sorted(sellers, key=itemgetter('Ventas'))
    """ print(sellers[0:5]) """
    return sellers[0:10]

def predict_best_sellers(month, year):
    sellers = []
    products = Product.query.filter_by(delete = False)
    for item in products:
        sellers.append({ "year": year, "month": month, "product": item.name.title(), "Ventas": round(predict(int(year), int(month), float(item.code)), 0) })
    sellers = sorted(sellers, key=itemgetter('Ventas'), reverse=True)
    """ print(sellers[0:5]) """
    return sellers[0:10]

def predict_worst_amounts(month, year):
    amounts = []
    total = 0
    products = Product.query.filter_by(delete = False)
    for item in products:
        ## OJO Aqui va 0 en el else
        amount = round(predict(int(year), int(month), float(item.code)), 2) if (predict(int(year), int(month), float(item.code))>0) else 0
        amounts.append({ "year": year, "month": month, "product": item.name.title(), "amount": round((amount*item.price), 2) })
    amounts = sorted(amounts, key=itemgetter('amount'))
    return {"total": total, "data": amounts[0:10]}

def predict_best_amounts(month, year):
    amounts = []
    total = 0
    products = Product.query.filter_by(delete = False)
    for item in products:
        amount = round(predict(int(year), int(month), float(item.code)), 2) if (predict(int(year), int(month), float(item.code))>0) else 0
        amounts.append({ "year": year, "month": month, "product": item.name.title(), "amount": round((amount*item.price), 2) })
    amounts = sorted(amounts, key=itemgetter('amount'), reverse=True)
    return {"total": total, "data": amounts[0:10]}

def predict_product_sell_variation(code, year):
    report = []
    for index, item in enumerate(months_labels):
        month = index + 1
        sales = round(predict(year, month, code), 2) if (predict(year, month, code)>0) else 0
        report.append({ "month": item, "ventas": round(sales, 0) })
    return report

