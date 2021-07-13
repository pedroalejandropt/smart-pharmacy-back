from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:pedro0310@localhost/tesis-db"
## app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:marie1408@localhost/tesis-db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
## app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "NumVecQ1Rz7zB4x3eavTeKnFI4AcR10FgM2tXF2TLu8m1ARCbZtmI3z-LedRzz81"

db = SQLAlchemy(app)


