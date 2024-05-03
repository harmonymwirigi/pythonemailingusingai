from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
import stripe
from werkzeug.security import check_password_hash

Base  = declarative_base()

db = SQLAlchemy()

class Adminuser(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    openai_key = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80),nullable=True)
    compaign = db.relationship('Compaign', backref='my_compain')
    password = db.Column(db.String(128), nullable=True)
    
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

class User(db.Model,Base):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    customer_id = db.Column(db.String(200), nullable = True)
    payment_intent_id = db.Column(db.String(200), nullable = True)
    amount = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Integer, nullable= True)
    compaign_id = db.Column(db.Integer, db.ForeignKey('compaign.id'))


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



