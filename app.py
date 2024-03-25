from flask import Flask
from flask_wtf.csrf import CSRFProtect
from auth.route import auth_bp
from user.route import user_bp
from auth.model import db

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mailing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

csrf = CSRFProtect(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
