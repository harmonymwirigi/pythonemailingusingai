from flask import Blueprint, render_template,redirect,url_for
from auth.forms import LoginForm, RegistrationForm
from auth.model import User, db
from emails.models import EmailTemplate
from emails.forms import Emailstemplate

user_bp = Blueprint('users', __name__)

@user_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = Emailstemplate()
    if form.validate_on_submit():
        # This block will execute when the form is submitted and all fields pass validation
        # Access form data using form.field_name.data
        header = form.Header.data
        body = form.body.data
        footer = form.footer.data
        print(footer)
        # Create a new EmailTemplate instance
        email_template = EmailTemplate(header=header, body=body, footer=footer)
        # Add the new EmailTemplate instance to the database session
        db.session.add(email_template)
        # Commit the changes to the database
        db.session.commit()
       
        return redirect(url_for('users.dashboard'))  # Redirect to the dashboard to clear the form
    else:
        # This block will execute when the form validation fails
        print('Form validation failed. Please ches.', 'error')  # Flash an error message
    
    # If the form is not submitted or validation fails, render the dashboard template with the form
    return render_template('dashboard.html', formu=form)