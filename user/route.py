from flask import Blueprint, render_template,redirect,url_for, request, flash
from auth.forms import LoginForm, RegistrationForm
from auth.model import User, db
from emails.models import EmailTemplate
from emails.forms import Emailstemplate
from compaign.model import Compaign
from user.forms import Generateform,OpenAiform, CompaignForm
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from openai import OpenAI

user_bp = Blueprint('users', __name__)


@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
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
    # If the form is not submitted or validation fails, render the dashboard template with the form
    return render_template('dashboard.html', formu=form, email_templates = email_templates, tempform = tempform, email=email, keyform=keyform, compainform = compainform, compains = compains)

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

@user_bp.route('/config', methods=['POST'])
@login_required
def config():
    form = OpenAiform()
    if form.validate_on_submit():
        key = form.key.data
        # Assuming you have SQLAlchemy and a User model
        current_user.openai_key = key
        db.session.commit()  # Save the changes to t
        return redirect(url_for('users.dashboard'))

@user_bp.route('/addcompaign', methods = ['POST'])
@login_required
def addcompaign():
    form = CompaignForm()
    if  form.validate_on_submit():
        name = form.name.data
        compain = Compaign(
            name = name,
            owner_id = current_user.id
        )
        # Add the new user to the database session
        db.session.add(compain)
        # Commit changes to the database
        db.session.commit()
        # Redirect to the login page after successful registration
        return redirect(url_for('users.dashboard'))


# dcqw whew eoyq gyki
@user_bp.route('/generate_email_body', methods=['POST'])
@login_required
def generate_email_body():
    # Retrieve template ID from request (assuming it's sent via POST)
    template_id = int(request.form.get('template_id'))  # Convert to integer
    # Provide your OpenAI API key here
    api_key = current_user.openai_key

    client = OpenAI(api_key=api_key)

    # Fetch email template from your database based on the template ID
    # Replace this with your actual database retrieval logic
    email_template = retrieve_email_template_from_database(template_id)
    # Construct prompt for OpenAI API instructing to generate an email with specific parts
    prompt = f"Generate an email with the following parts:\n\nHeader: {email_template.header}\n\nBody: {email_template.body}\n\nFooter: {email_template.footer}"
    completion = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens = 2400,
            temperature = 1
        )
    response_text = completion.choices[0].text

    
   # Fetch users from the database whose status is 2
    users = User.query.filter_by(status=2).all()

    # Send the generated email to each user
    for user in users:
        send_email(user.email, email_template.header, response_text)

    # Flash a success message
    flash("Emails sent successfully", "success")

    # Redirect to the dashboard
    return redirect(url_for('users.dashboard'))

    

@user_bp.route('/users')
@login_required
def users():
    form = Emailstemplate()
    keyform=OpenAiform()
    compainform = CompaignForm()
    users =  User.query.all()
    return render_template('users.html', users = users, formu = form,keyform=keyform, compainform = compainform)