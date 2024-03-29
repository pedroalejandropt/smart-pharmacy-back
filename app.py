from config import app, db
from Controllers.user_controller import api_user
from Controllers.role_controller import api_role
from Controllers.category_controller import api_category
from Controllers.subcategory_controller import api_subcategory

# Register the API
app.register_blueprint(api_role)
app.register_blueprint(api_user)
app.register_blueprint(api_category)
app.register_blueprint(api_subcategory)

@app.route('/')
def main_page():
    return "<html><head></head><body>A RESTful API in Flask using SQLAlchemy. For more info on usage, go to <a href>https://github.com/pedroalejandropt/tesis-api</a>.</body></html>"

with app.app_context():
    #db.drop_all()
    db.create_all()

if __name__ == '__main__':
    ''' run application '''
    app.run(host='0.0.0.0', port=5000)


