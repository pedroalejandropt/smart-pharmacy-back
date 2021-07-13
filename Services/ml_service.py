import numpy as np
import pandas as pd
from config import db
from Models.sale import Sale
from Models.product import Product
from werkzeug.exceptions import NotFound
from Models.product_sale import Product_Sale
from sklearn import linear_model, tree, ensemble
from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error

data = {'Year': [], 'Month': [], 'Sales': [], 'Code': []}

# Multiple Linear Regression
""" regr = linear_model.LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False) """

# Multiple Linear Regression Initial Fitting
""" def initial_train():
    ml_data = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Sale.year, Sale.month, Sale.sales_number)
        .order_by(Sale.year)
        .order_by(Sale.month)
        .order_by(Product.code)
        ).all()
    if len(ml_data) > 0:
        for item in ml_data:
            data['Year'].append(item.year)
            data['Month'].append(item.month)
            data['Sales'].append(item.sales_number)
            data['Code'].append(item.code)

        df = pd.DataFrame(data,columns=['Year','Month','Sales','Code'])
        X = df[['Year','Month', 'Code']].astype(float)
        Y = df['Sales'].astype(float)
        regr.fit(X, Y) """

# Predict using Multiple Linear Regression
""" def predict(year, month, code):
    result = regr.predict([[year, month, code]])
    return result[0] """


# Desition Tree
clf = tree.DecisionTreeRegressor(max_depth=25)

# Desition Tree Initial Fitting
def initial_train():
    ml_data = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Sale.year, Sale.month, Sale.sales_number)
        .order_by(Sale.year)
        .order_by(Sale.month)
        .order_by(Product.code)
        ).all()
    if len(ml_data) > 0:
        for item in ml_data:
            data['Year'].append(item.year)
            data['Month'].append(item.month)
            data['Sales'].append(item.sales_number)
            data['Code'].append(item.code)
        df = pd.DataFrame(data,columns=['Year','Month','Sales','Code'])
        X = df[['Year','Month', 'Code']].astype(float)
        Y = df['Sales'].astype(float)        
        clf.fit(X, Y)

# Predict using Desition Tree
def predict(year, month, code):
    result = clf.predict([[year, month, code]])
    return result[0]


# AdaBoost
""" adaboost = ensemble.AdaBoostRegressor(tree.DecisionTreeRegressor(max_depth=40), n_estimators=600, learning_rate=1) """

# AdaBoost Initial Fitting
""" def initial_train():
    ml_data = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Sale.year, Sale.month, Sale.sales_number)
        .order_by(Sale.year)
        .order_by(Sale.month)
        .order_by(Product.code)
        ).all()
    if len(ml_data) > 0:
        for item in ml_data:
            data['Year'].append(item.year)
            data['Month'].append(item.month)
            data['Sales'].append(item.sales_number)
            data['Code'].append(item.code)

        df = pd.DataFrame(data,columns=['Year','Month','Sales','Code'])
        X = df[['Year','Month', 'Code']].astype(float)
        Y = df['Sales'].astype(float)
        adaboost.fit(X, Y) """

# Predict using AdaBoost
""" def predict(year, month, code):
    result = adaboost.predict([[year, month, code]])
    return result[0] """


# Random Forest
""" rand = ensemble.RandomForestRegressor(max_depth=40, random_state=0, n_estimators=600) """

# Random Forest Initial Fiting
""" def initial_train():
    ml_data = (Sale.query.join(Product_Sale, Sale.id == Product_Sale.sale_id)
        .join(Product, Product_Sale.product_id == Product.id)
        .add_columns(Product.code, Sale.year, Sale.month, Sale.sales_number)
        .order_by(Sale.year)
        .order_by(Sale.month)
        .order_by(Product.code)
        ).all()
    if len(ml_data) > 0:
        for item in ml_data:
            data['Year'].append(item.year)
            data['Month'].append(item.month)
            data['Sales'].append(item.sales_number)
            data['Code'].append(item.code)

        df = pd.DataFrame(data,columns=['Year','Month','Sales','Code'])
        X = df[['Year','Month', 'Code']].astype(float)
        Y = df['Sales'].astype(float)
        rand.fit(X, Y) """

# Predict using Random Forest
""" def predict(year, month, code):
    result = rand.predict([[year, month, code]])
    return result[0] """


def train_from_file(year, month, product, sales):
    data_train = {'Year': [], 'Month': [], 'Sales': [], 'Code': []}
    data_train['Year'].append(year)
    data_train['Month'].append(month)
    data_train['Sales'].append(sales.sales_number)
    data_train['Code'].append(product.code)
    df = pd.DataFrame(data_train,columns=['Year','Month','Sales','Code'])
    X = df[['Year','Month', 'Code']].astype(float)
    Y = df['Sales'].astype(float)
    clf.fit(X, Y)

def coef():
    res1 = regr.predict([[2021, 1, 50015]])
    res2 = regr.predict([[2021, 2, 50015]])

    r2 = regr.score([[2021, 1, 50015],[2021, 2, 50015]], [res1,res2])
    print(r2)

def check_errors():
    y = clf.predict([[2021, 1, 50348]])
    print("""
Errores Algoritmo Decision Tree
    """)
    print('Mean Absolute Error:', mean_absolute_error([212], y)/1000)
    print('Mean Squared Error:', mean_squared_error([212], y)/1000000)
    print('Root Mean Squared Error:', np.sqrt(mean_squared_error([212], y))/1000)
    print('\n')