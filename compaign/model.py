from auth.model import db,Base
from flask_login import UserMixin

class Compaign(db.Model,UserMixin):
    __tablename__ = 'compaign'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    open_api_key = db.Column(db.String(255), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('adminuser.id'))
    users = db.relationship('User', backref='subscribers')
    url = db.Column(db.String(500), nullable = True)
    color = db.Column(db.String(50), nullable = True)
    title = db.Column(db.String(100), nullable = True)
    price = db.Column(db.Float(6,2), nullable = True)

    def __repr__(self):
        return f"<compain(name='{self.name}'"

