from Models.product import Product
from Models.sale import Sale
from Models.product_sale import Product_Sale
from config import db
from werkzeug.exceptions import NotFound
from sklearn import linear_model
import pandas as pd


regr = linear_model.LinearRegression()

data = {'Year': [], 'Month': [], 'Sales': [], 'Code': []}

def initial_train():
    ml_data = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Sale.year, Sale.month, Sale.salesNumber)
        .order_by(Sale.year)
        .order_by(Sale.month)
        .order_by(Product.code)
        ).all()
    if len(ml_data) > 0:
        for item in ml_data:
            data['Year'].append(item.year)
            data['Month'].append(item.month)
            data['Sales'].append(item.salesNumber)
            data['Code'].append(item.code)

        df = pd.DataFrame(data,columns=['Year','Month','Sales','Code'])
        X = df[['Year','Month', 'Code']].astype(float)
        Y = df['Sales'].astype(float)
        regr.fit(X, Y)

def train(year, month, product, sales):
    print('training')
    data_train = {'Year': [], 'Month': [], 'Sales': [], 'Code': []}
    data_train['Year'].append(year)
    data_train['Month'].append(month)
    data_train['Sales'].append(sales.salesNumber)
    data_train['Code'].append(product.code)
    df = pd.DataFrame(data_train,columns=['Year','Month','Sales','Code'])
    X = df[['Year','Month', 'Code']].astype(float)
    Y = df['Sales'].astype(float)
    regr.fit(X, Y)
    """ print(result[0]) """

def predict(year, month, code):
    result = regr.predict([[year, month, code]])
    return result[0]
    """ print(result[0]) """

def coef():
    res1 = regr.predict([[2021, 1, 12345]])
    res2 = regr.predict([[2021, 2, 12345]])

    r2 = regr.score([[2021, 1, 12345],[2021, 2, 12345]], [res1,res2])
    print(r2)



