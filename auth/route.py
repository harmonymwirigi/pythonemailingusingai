# auth.py
from flask import Blueprint, redirect,render_template,url_for,request, flash, abort,jsonify
from auth.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash
from flask import render_template
from auth.model import User, db,Adminuser
from compaign.model import Compaign
import stripe
import datetime
from flask import session
from flask_login import login_user, logout_user, login_required
key = "sk_test_51OtZ2hDpVKhl93DHXsSMIbtcVTK8DIGS5Tt5dznFjBlmy8kq1006rdkHsH272Qsy94Oo08YXXo0YgMm3TT4H0FJ500rEd5CIXd"
product = "prod_Pk06dC0dgMFlxX"
# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_8YBO1XbqNGKjcSSqkpHaON8zTbcozZci'



def create_customer(email, key):
    # Initialize the Stripe API with your secret key
    stripe.api_key = key

    # Create a customer
    customer = stripe.Customer.create(
        email=email,
    )

    return customer.id
def create_default_price_and_update_product(product_id, unit_amount, key):
    try:
        # Initialize the Stripe API with your secret key
        stripe.api_key = key

        # Create a new price
        new_price = stripe.Price.create(
            product=product_id,
            unit_amount=unit_amount,  # Amount in cents
            currency="usd",
        )

        # Update the product's default price
        stripe.Product.modify(
            product_id,
            default_price=new_price.id
        )

        return new_price.id  # Return the ID of the created price
    except stripe.error.StripeError as e:
        print("Stripe Error:", e)
        return None

def create_checkout_session(success_url, price_id, api_key, customer=None, quantity=1):
    try:
        # Initialize the Stripe API with your secret key
        stripe.api_key = api_key

        # Create a checkout session
        session = stripe.checkout.Session.create(
            success_url=success_url,
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": quantity}],
            mode="payment",
            customer=customer  # Optionally associate the session with a customer
        )

        return session.url  # Return the URL of the created checkout session
    except stripe.error.StripeError as e:
        print("Stripe Error:", e)
        return None


# Define a Flask Blueprint named 'auth_bp'
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    if request.method == "POST":
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        # Handle the event
        if event['type'] == 'account.updated':
            account = event['data']['object']
        elif event['type'] == 'account.external_account.created':
            external_account = event['data']['object']
        elif event['type'] == 'account.external_account.deleted':
            external_account = event['data']['object']
        elif event['type'] == 'account.external_account.updated':
            external_account = event['data']['object']
        elif event['type'] == 'balance.available':
            balance = event['data']['object']
        elif event['type'] == 'billing_portal.configuration.created':
            configuration = event['data']['object']
        elif event['type'] == 'billing_portal.configuration.updated':
            configuration = event['data']['object']
        elif event['type'] == 'billing_portal.session.created':
            session = event['data']['object']
        elif event['type'] == 'capability.updated':
            capability = event['data']['object']
        elif event['type'] == 'cash_balance.funds_available':
            cash_balance = event['data']['object']
        elif event['type'] == 'charge.captured':
            charge = event['data']['object']
        elif event['type'] == 'charge.expired':
            charge = event['data']['object']
        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            paymentintent_id = payment_intent['id']
            customer = payment_intent['customer']
            amount = payment_intent['amount_received'] / 100
            
            try:
                # Assuming you have a Payments model with appropriate fields
                payment = User.query.filter_by(customer_id=customer).first()
                if payment:
                    payment.payment_intent_id = paymentintent_id
                    payment.amount = amount
                    payment.status = 2
                    db.session.commit()
            except Exception as e:
                # Handle database update error
                print("Database update error:", e)
           
        return jsonify(success=True)

@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Retrieve the user based on the provided email
        user = Adminuser.query.filter_by(email=form.email.data).first()
        if user:
            # Check if the password is correct
            # print(user.check_password(form.password.data))
            if user.password ==form.password.data:
                
                    login_user(user)
                    
                    # If the user is an admin, redirect to the admin dashboard
                    return redirect(url_for('users.dashboard'))
                      # Replace 'admin.dashboard' with the appropriate endpoinT
            else:
                print('Incorrect password. Please try again.')
                flash('Incorrect password. Please try again.', 'danger')
        else:
            print('User does not exist. Please try again.')
            flash('User does not exist. Please try again.', 'danger')
    
    # Render the login template with the login form
    return render_template('login.html', form=form )

@auth_bp.route('/success')
def success():
    return render_template('success.html')

@auth_bp.route('/logout')
def logout():
    # Log out the user
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register/<code>', methods=['GET', 'POST'])
def register(code):
    compaign = Compaign.query.filter_by(url=code).first()
    color = compaign.color
    title = compaign.title
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash the password before storing it in the database
        # Create a new user instance with form data and hashed password
        created_customer = create_customer(form.email.data, key)
        
        unit_amount = 10000  # Replace with your desired unit amount in cents
        created_price_id = create_default_price_and_update_product(product, unit_amount, key)
        # Example usage:
        success_url = "http://ec2-43-204-130-254.ap-south-1.compute.amazonaws.com/auth/success"

        

        quantity = 1  # Optional, default is 1
        checkout_session_url = create_checkout_session(success_url, created_price_id,key,customer=created_customer, quantity=quantity)
        new_user = User(
            email=form.email.data,
            customer_id= created_customer,
            amount = unit_amount, 
            status= 1,
            compaign_id = compaign.id
                # Store the hashed password in the database
        )
        # Add the new user to the database session
        db.session.add(new_user)
        # Commit changes to the database
        db.session.commit()
        # Redirect to the login page after successful registration
        return redirect(checkout_session_url)
    # Render the registration form template
    return render_template('register.html', form=form, color = color,title = title, code = code)

@auth_bp.route('/admin_register', methods=['GET', 'POST'])
def register_admin():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hashed_password = generate_password_hash(form.password.data)
        new_admin = Adminuser(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin user created successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('admin_register.html', form=form)

