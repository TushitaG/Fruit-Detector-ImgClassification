from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Sign In')