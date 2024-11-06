from flask import Flask, redirect, url_for
from client.routes.auth_routes import auth 
from client.routes.public_routes import public 
from client.utils.database_connection import db
from dotenv import load_dotenv
from flask_migrate import Migrate

import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(public, url_prefix='/public') 
app.register_blueprint(auth, url_prefix='/auth')

@app.route('/')
def home_redirect():
    return redirect(url_for('public.home'))  # Assuming 'home' is the function name in `public_routes.py`

if __name__ == '__main__':
    app.run(debug=True)