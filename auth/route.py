# auth.py
from flask import Blueprint, redirect,render_template,url_for,request, flash
from auth.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash
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
        if user:
            # Check if the password is correct
            if user.check_password(form.password.data):
                if user.is_admin:
                    # If the user is an admin, redirect to the admin dashboard
                    return redirect(url_for('admin.dashboard'))  # Replace 'admin.dashboard' with the appropriate endpoint
                else:
                    # If the user is not an admin, redirect to the user dashboard
                    return redirect(url_for('user.dashboard'))  # Replace 'user.dashboard' with the appropriate endpoint
            else:
                flash('Incorrect password. Please try again.', 'danger')
        else:
            flash('User does not exist. Please try again.', 'danger')
    
    # Render the login template with the login form
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(form.password.data)
        # Create a new user instance with form data and hashed password
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password  # Store the hashed password in the database
        )
        # Add the new user to the database session
        db.session.add(new_user)
        # Commit changes to the database
        db.session.commit()
        # Redirect to the login page after successful registration
        return redirect(url_for('auth.login'))
    # Render the registration form template
    return render_template('register.html', form=form)

@auth_bp.route('/admin_register', methods=['GET', 'POST'])
def register_admin():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_admin = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            is_admin=True
        )
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin user created successfully!', 'success')
        return redirect(url_for('user.dashboard'))
    return render_template('admin_register.html', form=form)

# Define a route for the logout functionality
@auth_bp.route('/logout')
def logout():
    return 'Logout Page'
