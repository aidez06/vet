from flask import Flask, redirect, url_for, session
from admin.routes.auth_routes import auth_admin
from admin.routes.dashboard_routes import dashboard_admin
from client.routes.auth_routes import auth 
from client.routes.public_routes import public 
from client.routes.booking_routes import book
from client.utils.database_connection import db
from dotenv import load_dotenv
from flask_migrate import Migrate
from datetime import timedelta

import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Initialize the database with the app
db.init_app(app)
migrate = Migrate(app, db)

# Automatically create tables if they don't exist
with app.app_context():
    db.create_all()
@app.before_request
def make_session_permanent():
    session.permanent = True  # Make the session permanent
app.register_blueprint(public, url_prefix='/public') 
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(auth_admin, url_prefix='/admin')
app.register_blueprint(dashboard_admin, url_prefix='/admin')
app.register_blueprint(book)

@app.route('/')
def home_redirect():
    return redirect(url_for('public.home'))  # Assuming 'home' is the function name in `public_routes.py`

if __name__ == '__main__':
    app.run(debug=True)