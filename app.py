from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db, User, Task
from dotenv import load_dotenv
from os import path, environ
from flask_mail import Mail
from flask_login import LoginManager, login_required, logout_user
from forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash


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

# Instantiating Mail from flask_email
mail = Mail(app)

# Instantiating LoginManager
login_manager = LoginManager()

#Initializing the login_manager extension with the application
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/register' , methods = ['GET', 'POST'])
def register():
    register_form = RegistrationForm()
 
    if register_form.validate_on_submit():
        hashed_password = generate_password_hash(register_form.password.data, method = 'sha256')
        username = register_form.username.data
        email = register_form.email.data
        password = hashed_password
 
 
        new_user = User(name=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
 
        flash("Registration was successfull!", "success")
 
        return redirect(url_for('login'))
 
 
    return render_template('register.html', form=register_form)

@app.route('/login')
def login():
    login_form = LoginForm()
    return render_template("login.html", form=login_form)


# Run application
if __name__ == '__main__':
    app.run(debug=True)