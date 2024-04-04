from flask import Flask
from flask_wtf.csrf import CSRFProtect
from auth.route import auth_bp
from user.route import user_bp
<<<<<<< HEAD
from auth.model import db, User
from flask_admin import Admin
from emails.models import EmailTemplate
from flask_admin.contrib.sqla import ModelView
import stripe

=======
from mails.model import Mails
from flask_admin.contrib.sqla import ModelView

from auth.model import db,User
from flask_admin import Admin
>>>>>>> e337274e02ad533c64c37692876243ca90323950


app = Flask(__name__)
admin = Admin()
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mailing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask extensions
db.init_app(app)
admin.init_app(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(EmailTemplate, db.session))


  # Initialize Flask-Admin with your app
admin = Admin()

# Register the blueprint with your Flask application
admin.init_app(app)
# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
<<<<<<< HEAD
# app.register_blueprint(admin_bp, url_prefix='/admin')
=======
# Register Flask-Admin views for your models
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Mails, db.session))

>>>>>>> e337274e02ad533c64c37692876243ca90323950

if __name__ == "__main__":
    with app.app_context():
        # Create database tables
        db.create_all()
    app.run(debug=True)
