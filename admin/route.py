from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from auth.model import User,db

admin_bp = Blueprint('admin', __name__)
