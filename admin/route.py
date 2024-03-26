from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from auth.model import User,db

admin_bp = Blueprint('admin', __name__)
admin = Admin()

# Register Flask-Admin views for your models
admin.add_view(ModelView(User, db.session))

# Register the blueprint with your Flask application
admin.init_app(admin_bp)
