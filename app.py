# app.py

from flask import Flask
from auth.route import auth_bp
from flask_wtf.csrf import CSRFProtect
from flask import Flask, redirect, url_for


app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.config['SECRET_KEY'] = 'your_secret_key_here'

csrf = CSRFProtect(app)

if __name__ == "__main__":
    app.run(debug=True)
