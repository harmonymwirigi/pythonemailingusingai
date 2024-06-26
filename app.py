from flask import Flask
from flask_wtf.csrf import CSRFProtect
from auth.route import auth_bp
from user.route import user_bp
from compaign.route import compaigns
from auth.model import db, User, Adminuser
from compaign.model import Compaign
from flask_admin import Admin
from emails.models import EmailTemplate
from flask_admin.contrib.sqla import ModelView
import stripe
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin



app = Flask(__name__)
admin = Admin()
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Harmo36840568@mailingsolution.c1oku62s0o5m.ap-south-1.rds.amazonaws.com/mailing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User loader function required by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Adminuser.query.filter_by(id=user_id).first()

# Initialize Flask extensions
db.init_app(app)
admin.init_app(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(EmailTemplate, db.session))
admin.add_view(ModelView(Compaign, db.session))


  # Initialize Flask-Admin with your app
# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(compaigns, url_prefix='/compaign')
# app.register_blueprint(admin_bp, url_prefix='/admin')


if __name__ == "__main__":
   
    app.run(debug=True)
