# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField,TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class Generateform(FlaskForm):
    id = IntegerField('tempid')