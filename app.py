from flask import Flask, render_template_string
from flask_security import Security, SQLAlchemySessionUserDatastore, current_user, auth_required, hash_password
from database import db, User, Task, Role
from dotenv import load_dotenv
from os import path, environ


# Flask App Initialization
app = Flask(__name__)

# Load the environment variables from the .env file
load_dotenv()

basedir = path.abspath(path.dirname(__file__))

# Configuring database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'flask_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

#Initializing the database extension with the application
db.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(app, User, Role)
security = Security(app, user_datastore)

@app.route('/')
@auth_required()
def home():
    return render_template_string(f"Hello, {{current_user.email}}")


# Run application
if __name__ == '__main__':
    app.run(debug=True)