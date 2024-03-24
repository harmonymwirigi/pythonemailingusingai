# auth.py
from flask import Blueprint
from auth.forms import LoginForm, RegistrationForm
from flask import render_template

# Define a Flask Blueprint named 'auth_bp'
auth_bp = Blueprint('auth', __name__)

# Define a route for the login functionality
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return None
        # Process the form data (e.g., authenticate user)
        # Redirect to another page
    
    return render_template('login.html', form=form)

@auth_bp.route('/register')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process the form data (e.g., store user in database)
        return redirect(url_for('login'))  # Redirect to login page after successful registration
    return render_template('register.html', form=form)
# Define a route for the logout functionality
@auth_bp.route('/logout')
def logout():
    return 'Logout Page'
