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

    # Define the HTML content of the email
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                padding: 20px;
            }}
            .email-container {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .body {{
                font-size: 16px;
                line-height: 1.5;
                
            }}
            .footer {{
                font-size: 14px;
                color: #777;
                height: 60px;
                text-align: center;
                background-color: black;
            }}
            .footer-content{{
                padding-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                Animal news of Dogs 
            </div>
            <img src="/static/images/periodico.png" height="100px" width="90px">
            <br>
            <br>
            <div class="body">
            {body}
            <div class="footer">
                
                <p class="footer-content">&copy; 2024 Your Company. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Attach the email body as HTML
    message.attach(MIMEText(html_content, 'html'))

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
    code = this_campaign.url
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
                           url = code,
                           active_compaign_id=int(compaign))  # Pass active_compaign_id to the template



@compaigns.route('/customize/<campaign>', methods =['POST', 'GET'])
def customize(campaign):
    customizeform = Customizeform()
    if customizeform.validate_on_submit():
        title = customizeform.title.data
        color = customizeform.color.data
        price = customizeform.price.data
        customize = Compaign.query.filter_by(id=campaign).first()
        customize.title  = title
        customize.color = color
        customize.price = price
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
    code = this_campaign.url
    check_key = this_campaign.open_api_key
    return render_template('compaignusers.html',active_compaign_id=int(id),url = code, users = users,compaign_id=compaign_id,check_key =check_key, compains=compains,customizeform = customizeform, formu = form,keyform=keyform, compainform = compainform)

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

# dcqw whew eoyq gyki
@compaigns.route('/generate_email_body/<compaign>', methods=['POST'])
@login_required
def generate_email_body(compaign):
    # Retrieve template ID from request (assuming it's sent via POST)
    template_id = int(request.form.get('template_id'))  # Convert to integer
    compain = Compaign.query.filter_by(id = compaign).first()
    # Provide your OpenAI API key here
    api_key = compain.open_api_key

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
    users = User.query.filter_by(status=1).all()

    # Send the generated email to each user
    for user in users:
        send_email(user.email, email_template.header, response_text)

    # Flash a success message
    flash("Emails sent successfully", "success")

    # Redirect to the dashboard
    return redirect(url_for('users.dashboard'))

    
 
