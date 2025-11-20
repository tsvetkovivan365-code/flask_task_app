from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, DateField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], render_kw={"placeholder": "Enter Username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Enter Password"})

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Enter Username"})
    email = EmailField('Email', validators=[DataRequired()], render_kw={"placeholder": "Enter Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Enter Password"})


    
class CreateTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[Length(max=100)])
    due_date = DateField('Due Date', validators=[DataRequired()])
    status = RadioField('Status', choices=["To Do", "In Progress", "Completed"])
    priority = RadioField('Priority', choices=["Low", "Medium", "High", "Critical"])