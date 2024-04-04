# auth.py
from flask import Blueprint, redirect,render_template,url_for,request, flash
from auth.forms import LoginForm, RegistrationForm
from flask import render_template
from auth.model import User, db


# Define a Flask Blueprint named 'auth_bp'
user_bp = Blueprint('users', __name__)

@user_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    return render_template('dashboad.html')