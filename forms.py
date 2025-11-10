from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Enter Username"})
    password = PasswordField('Password', render_kw={"placeholder": "Enter Password"})

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], render_kw={"placeholder": "Enter Username"})
    email = EmailField('Email', validators=[InputRequired()], render_kw={"placeholder": "Enter Email"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8) ], render_kw={"placeholder": "Enter Password"})
    