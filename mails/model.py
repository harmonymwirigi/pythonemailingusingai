from auth.route import db

class Mails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(80), unique=True, nullable=False)
    email_body = db.Column(db.String(20000), unique=True, nullable=False)
    footer = db.Column(db.String(2000), nullable=False)
    
    def __repr__(self):
        return self.head