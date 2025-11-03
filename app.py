from flask import Flask
from database import db

# Flask App Initialization
app = Flask(__name__)

# Configuring database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

#Initializing the database extension with the application
db.init_app(app)
