# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class Emailstemplate(FlaskForm):
    Header = StringField('header', validators=[DataRequired()])
    body = StringField('Email address', validators=[DataRequired()])
    footer = StringField('Footer', validators=[DataRequired()])
    add = BooleanField('Submit')
