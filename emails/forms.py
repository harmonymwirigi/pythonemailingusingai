# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class Emailstemplate(FlaskForm):
    Header = StringField('header')
    body = TextAreaField('Body', )
    footer = StringField('Footer')
