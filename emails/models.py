from auth.model import db,Base
from flask_login import UserMixin

class EmailTemplate(db.Model,UserMixin):
    __tablename__ = 'email_templates'

    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(255), nullable=True)
    body = db.Column(db.Text, nullable=False)
    footer = db.Column(db.Text, nullable=False)
    compaign = db.Column(db.Integer, nullable = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('adminuser.id'))

    def __repr__(self):
        return f"<EmailTemplate(name='{self.header}'"
