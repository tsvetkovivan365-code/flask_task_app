from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db, User, Task
from dotenv import load_dotenv
from os import path, environ
from flask_mail import Mail
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired


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
def dashboard():
    return render_template("dashboard.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if not name or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))
        existing_user = User.query.filter_by(email="email").first()
        if existing_user:
            flash("Email already exists!", 'error')
            return redirect(url_for('register'))
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("You have successfully registered!", 'success')
        return redirect(url_for('dashboard.html'))
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")


# Run application
if __name__ == '__main__':
    app.run(debug=True)