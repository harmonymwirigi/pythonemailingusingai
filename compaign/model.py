from auth.model import db,Base
from flask_login import UserMixin

class Compaign(db.Model,UserMixin):
    __tablename__ = 'compaign'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    open_api_key = db.Column(db.String(255), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('adminuser.id'))
    users = db.relationship('User', backref='subscribers')

    def __repr__(self):
        return f"<compain(name='{self.name}'"
