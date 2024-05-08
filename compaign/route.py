from flask import Blueprint, render_template,redirect,url_for, request, flash
from auth.forms import LoginForm, RegistrationForm
from auth.model import User, db
from compaign.model import Compaign
from emails.models import EmailTemplate
from emails.forms import Emailstemplate
from compaign.forms import Customizeform
from user.forms import Generateform,OpenAiform, CompaignForm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from openai import OpenAI

compaigns = Blueprint('compaigns', __name__)
def retrieve_email_template_from_database(template_id):
    # Query the database to retrieve the email template by ID
    email_template = EmailTemplate.query.filter_by(id=template_id).first()
    return email_template
def send_email(recipient, subject, body):
    # Configure SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'harmonymwirigi99@gmail.com'
    sender_password = 'dcqw whew eoyq gyki'

    # Create a MIME multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject

    # Attach the email body as plain text
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)


@compaigns.route('/<compaign>', methods=['GET', 'POST'])
@login_required
def dashboard(compaign):
    customizeform = Customizeform()
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
        
        # Create a new EmailTemplate instance
        email_template = EmailTemplate(header=header, body=body, footer=footer, owner_id = current_user.id, compaign = compaign)
        # Add the new EmailTemplate instance to the database session
        db.session.add(email_template)
        # Commit the changes to the database
        db.session.commit()
       
        return redirect(url_for('compaigns.dashboard', compaign = compaign))  # Redirect to the dashboard to clear the form
    else:
        # Handle form validation failure as before
        pass
    
    email_templates = EmailTemplate.query.filter_by(owner_id=current_user.id, compaign=compaign).all()
    compains = Compaign.query.filter_by(owner_id=current_user.id).all()
    this_campaign = Compaign.query.filter_by(id=compaign).first()
    check_key = this_campaign.open_api_key
    compaign_id = compaign
    db.session.commit() 
    
    
    return render_template('compaigndashboard.html', 
                           formu=form, 
                           email_templates=email_templates, 
                           tempform=tempform, 
                           email=email, 
                           keyform=keyform, 
                           compainform=compainform, 
                           compains=compains, 
                           compaign_id=compaign_id,
                           customizeform = customizeform, 
                           check_key=check_key,
                           active_compaign_id=int(compaign))  # Pass active_compaign_id to the template



@compaigns.route('/customize/<campaign>', methods =['POST', 'GET'])
def customize(campaign):
    customizeform = Customizeform()
    if customizeform.validate_on_submit():
        title = customizeform.title.data
        color = customizeform.color.data
        customize = Compaign.query.filter_by(id=campaign).first()
        customize.title  = title
        customize.color = color
        db.session.commit()
        return redirect(url_for('compaigns.dashboard',compaign = campaign))


@compaigns.route('/<id>/users')
@login_required
def users(id):
    customizeform = Customizeform()
    form = Emailstemplate()
    keyform=OpenAiform()
    compainform = CompaignForm()
    compaign_id =id
    users =  User.query.filter_by(compaign_id = id).all()
    compains = Compaign.query.filter_by(owner_id=current_user.id).all()
    this_campaign = Compaign.query.filter_by(id=id).first()
    check_key = this_campaign.open_api_key
    return render_template('compaignusers.html',active_compaign_id=int(id), users = users,compaign_id=compaign_id,check_key =check_key, compains=compains,customizeform = customizeform, formu = form,keyform=keyform, compainform = compainform)

@compaigns.route('/config/<id>', methods=['POST'])
@login_required
def config(id):
    form = OpenAiform()
    if form.validate_on_submit():
        key = form.key.data
        compain = Compaign.query.filter_by(id = id).first()
        compain.open_api_key = key
        db.session.commit()  # Save the changes to t
        return redirect(url_for('compaigns.dashboard', compaign = id))
    

    
