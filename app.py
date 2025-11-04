from flask import Flask
from database import db
from os import path

# Flask App Initialization
app = Flask(__name__)

basedir = path.abspath(path.dirname(__file__))

# Configuring database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'flask_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initializing the database extension with the application
db.init_app(app)

@app.route('/')
def index():
    return 'Flask is working'

