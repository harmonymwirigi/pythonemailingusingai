from flask import Blueprint, abort, session
from auth.model import User, db
from flask_admin.contrib.sqla import ModelView
from flask import  url_for, redirect, request
from flask_security import Security, SQLAlchemyUserDatastore, login_required, current_user
from flask_security.utils import encrypt_password
from flask_admin.contrib import sqla
from flask_admin import BaseView, expose


adm = Blueprint("adm", __name__)
        
    
admin.name = "Admin Panel"

class SecuredModel(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))
    
class SecureModel(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))



admin.add_view(AnalyticsView(name='VERIFY VEHICLE', endpoint='analytics'))


admin.add_view(SecuredModel(User, db.session))
