from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField,
    SubmitField,
)
from wtforms import ValidationError
from wtforms.validators import (
    DataRequired, Length, Email,
    Regexp, EqualTo,
)

from app.auth.models import User


class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')