from flask import Blueprint, render_template,redirect,url_for, request, flash
from auth.forms import LoginForm, RegistrationForm
from auth.model import User, db
from compaign.model import Compaign
from emails.models import EmailTemplate
from emails.forms import Emailstemplate
from user.forms import Generateform,OpenAiform, CompaignForm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from openai import OpenAI

compaigns = Blueprint('compaigns', __name__)

@compaigns.route('/<compaign>', methods=['GET', 'POST'])
@login_required
def dashboard(compaign):
    tempform = Generateform()
    form = Emailstemplate()
    keyform = OpenAiform()
    compainform = CompaignForm()
    email = current_user.email
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
    
     # Fetch all EmailTemplate instances from the database
    email_templates = EmailTemplate.query.all()
    compains = Compaign.query.filter_by(owner_id = current_user.id).all()
    this_campaign = Compaign.query.filter_by(id = compaign).first()
    check_key = this_campaign.open_api_key
    compaign_id = compaign
    # If the form is not submitted or validation fails, render the dashboard tem
    # If the form is not submitted or validation fails, render the dashboard template with the form
    return render_template('compaigndashboard.html', formu=form, email_templates = email_templates, tempform = tempform, email=email, keyform=keyform, compainform = compainform, compains =compains, compaign_id = compaign_id, check_key = check_key)

@compaigns.route('/compain/<id>/users')
def users(id):
    form = Emailstemplate()
    keyform=OpenAiform()
    compainform = CompaignForm()
    users =  User.query.filter_by(compaign_id = id).all()
    return render_template('users.html', users = users, formu = form,keyform=keyform, compainform = compainform)


