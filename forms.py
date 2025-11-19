from flask_wtf import FlaskForm
from database import db, User
from datetime import datetime
from wtforms import StringField, RadioField, DateField, EmailField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], render_kw={"placeholder": "Enter Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Enter Password"})

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Enter Username"})
    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Enter Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Enter Password"})

    def validate_username(self, username):
        user = db.session.execute(db.select(User).filter_by(username=username.data))
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
class CreateTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[Length(max=100)])
    due_date = DateField('Due Date', validators=[DataRequired()])
    status = RadioField('Status', choices=["To Do", "In Progress", "Completed"])
    priority = RadioField('Priority', choices=["Low", "Medium", "High", "Critical"])