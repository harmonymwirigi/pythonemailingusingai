from flask_sqlalchemy import SQLAlchemy
import stripe
from werkzeug.security import check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    customer_id = db.Column(db.String(200), nullable = True)
    payment_intent_id = db.Column(db.String(200), nullable = True)
    amount = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Integer, nullable= True)
    is_admin = db.Column(db.Boolean, default=False)


    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.id
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def get_id(self):
        return self.id



