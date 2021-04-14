from config import app, db
from Controllers.user_controller import api_user
from Controllers.role_controller import api_role
from Controllers.sale_controller import api_sale
from Controllers.report_controller import api_report
from Controllers.product_controller import api_product
from Controllers.exchange_controller import api_exchange
from Controllers.category_controller import api_category
from Controllers.parameter_controller import api_parameter
from Controllers.subcategory_controller import api_subcategory
from Services.ml_service import initial_train, predict, coef
from Services.report_service import *
from Models.user_parameter import cancel_schedule

# Register the API
app.register_blueprint(api_role)
app.register_blueprint(api_user)
app.register_blueprint(api_category)
app.register_blueprint(api_subcategory)
app.register_blueprint(api_product)
app.register_blueprint(api_exchange)
app.register_blueprint(api_sale)
app.register_blueprint(api_report)
app.register_blueprint(api_parameter)

@app.route('/')
def main_page():
    cancel_schedule()
    return "<html><head></head><body>A RESTful API in Flask using SQLAlchemy. For more info on usage, go to <a href>https://github.com/pedroalejandropt/tesis-api</a>.</body></html>"

with app.app_context():
    db.drop_all()
    db.create_all()
    initial_train()
    #coef()

if __name__ == '__main__':
    ''' run application '''
    app.run(host='0.0.0.0', port=5000)


