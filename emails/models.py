from auth.model import db

class EmailTemplate(db.Model):
    __tablename__ = 'email_templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    body = db.Column(db.Text, nullable=False)
    footer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<EmailTemplate(name='{self.name}', subject='{self.subject}')>"
