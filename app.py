from flask import Flask, render_template, redirect, url_for, flash, request
from database import db, User, Task
from dotenv import load_dotenv
from os import path, environ
from flask_mail import Mail
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from forms import LoginForm, RegistrationForm, CreateTaskForm
from werkzeug.security import generate_password_hash, check_password_hash
import sys


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

# Initializing LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/dashboard', methods = ['GET'])
@login_required
def dashboard():
 
    selected_status = request.args.get('selected_status')
    selected_priority = request.args.get('selected_priority')
 
    if selected_status and selected_priority:
        tasks = Task.query.filter_by(user_id=current_user.id, status=selected_status, priority=selected_priority).all()
    elif selected_status:
        tasks = Task.query.filter_by(user_id=current_user.id, status=selected_status).all()
    elif selected_priority:
        tasks = Task.query.filter_by(user_id=current_user.id, priority=selected_priority).all()
    else:
        tasks = Task.query.filter_by(user_id=current_user.id).all()

    return render_template("dashboard.html", tasks=tasks)

@app.route('/create_task', methods = ['GET', 'POST'])
@login_required
def create_task():
    create_task_form = CreateTaskForm()

    if create_task_form.validate_on_submit():
        title = create_task_form.title.data
        description = create_task_form.description.data
        due_date = create_task_form.due_date.data
        status = create_task_form.status.data
        priority = create_task_form.priority.data
        user_id = current_user.id
 
        new_task = Task(title=title, description=description, due_date=due_date, status=status, user_id=user_id, priority=priority)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('dashboard'))

    
    return render_template("create_task.html", form=create_task_form)

@app.route('/register' , methods = ['GET', 'POST'])
def register():
    register_form = RegistrationForm()
 
    if register_form.validate_on_submit():
        hashed_password = generate_password_hash(register_form.password.data)
        username = register_form.username.data
        email = register_form.email.data

        if User.query.filter_by(username=username).first():
            return render_template('register.html', form=register_form, error='Username already exists')
 
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
 
 
        return redirect(url_for('login'))
 
 
    return render_template('register.html', form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data 

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "error")
            return render_template('login.html', form=login_form, error="Invalid username or password")
        

    return render_template("login.html", form=login_form)

# DELETE task
@app.route('/api/tasks/delete', methods=['DELETE'])
@login_required
def api_delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
 
    db.session.delete(task)
    db.session.commit()
 
    return render_template("dashboard.html") 


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully!", 'success')
    return redirect(url_for('home'))

# Run application
if __name__ == '__main__':
    app.run(debug=True)

