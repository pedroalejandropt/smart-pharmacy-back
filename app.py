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
from Services.ml_service import initial_train, check_errors

import time
import math
import threading

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

""" class Timer():
    def __init__(self, time, time_seg):
        self.time = time
        self.time_seg = time_seg
    
    def set_time(self, time):
        self.time = time

    def set_time_seg(self, time_seg):
        self.time_seg = time_seg
    
    def get_time(self):
        return self.time

    def get_time_seg(self):
        return self.time_seg """

""" def timer():
    global timer_class
    timer_class = Timer(0, 0)
    cont = 0
    while True:
        cont += 1
        total_seg = timer_class.get_time_seg()
        minutes = math.trunc(total_seg/60) if total_seg > 60 else 0
        seconds = int(((total_seg/60) - minutes) * 60)
        countup = f'{minutes}:{seconds}'
        timer_class.set_time(countup)
        timer_class.set_time_seg(cont)
        time.sleep(1) """

@app.route('/')
def main_page():
    """ check_errors() """
    return "<html><head></head><body>A RESTful API in Flask using SQLAlchemy. For more info on usage, go to <a href>https://github.com/pedroalejandropt/tesis-api</a>.</body></html>"

with app.app_context():
    """ db.drop_all()
    db.create_all() """
    """ global timer_class
    t1 = threading.Thread(target=timer)
    t1.start() """
    initial_train()
    """ print('Tiempo de Entrenamiendo de Algoritmo Decision Tree es: ' + timer_class.get_time()) """

    

if __name__ == '__main__':
    ''' run application ''' 
    """ timer_class = Timer(0, 0) """
    app.run(host='0.0.0.0', port=5000)


