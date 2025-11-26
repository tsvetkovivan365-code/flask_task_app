from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, PasswordField, SelectField
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
    status = SelectField('Status', choices=[("To Do", "To Do"), ("In Progress", "In Progress"), ("Completed", "Completed")], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High"), ("Critical", "Critical")], validators=[DataRequired()])