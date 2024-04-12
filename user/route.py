from flask import Blueprint, render_template,redirect,url_for, request
from auth.forms import LoginForm, RegistrationForm
from auth.model import User, db
from emails.models import EmailTemplate
from emails.forms import Emailstemplate
from user.forms import Generateform

from openai import OpenAI

user_bp = Blueprint('users', __name__)

# Provide your OpenAI API key here
api_key = "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"

client = OpenAI(api_key=api_key)

@user_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    tempform = Generateform()
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
    
     # Fetch all EmailTemplate instances from the database
    email_templates = EmailTemplate.query.all()
    # If the form is not submitted or validation fails, render the dashboard template with the form
    return render_template('dashboard.html', formu=form, email_templates = email_templates, tempform = tempform)

def retrieve_email_template_from_database(template_id):
    # Query the database to retrieve the email template by ID
    email_template = EmailTemplate.query.filter_by(id=template_id).first()
    return email_template

@user_bp.route('/generate_email_body', methods=['POST'])
def generate_email_body():
    # Retrieve template ID from request (assuming it's sent via POST)
    template_id = int(request.form.get('template_id'))  # Convert to integer

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


    

    # Replace placeholders in the template with the generated content
    email_template_with_generated_content = email_template.body.replace('{{content}}', response_text)

    # You can now use the email_template_with_generated_content to send the email or return it as a response
    return response_text

@user_bp.route('/users')
def users():
    form = Emailstemplate()
    users = User.query.all()
    return render_template('users.html', users = users, formu = form)