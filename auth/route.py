# auth.py
from flask import Blueprint, redirect,render_template,url_for,request, flash
from auth.forms import LoginForm, RegistrationForm
from flask import render_template
from auth.model import User, db

# Define a Flask Blueprint named 'auth_bp'
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Retrieve the user based on the provided email
        user = User.query.filter_by(email=form.email.data).first()
        # Check if the user exists and the password is correct
        if user and user.check_password(form.password.data):
            # If authentication succeeds, redirect to the dashboard or home page
            # Redirect to another page
            return redirect(url_for('user.dashboard'))  # Replace 'dashboard' with the appropriate endpoint
        else:
            # If authentication fails, display an error message
            flash('Invalid email or password. Please try again.', 'danger')
            # You can customize the error message and the 'danger' category as needed

    # Render the login template with the login form
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user instance with form data
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        # Add the new user to the database session
        db.session.add(new_user)
        # Commit changes to the database
        db.session.commit()
        # Redirect to the login page after successful registration
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
# Define a route for the logout functionality
@auth_bp.route('/logout')
def logout():
    return 'Logout Page'
