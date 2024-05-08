# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField,TextAreaField, ColorField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class Customizeform(FlaskForm):
    title = StringField('Title')
    color = ColorField('Color', )
    
