from flask import (request, render_template, 
                   url_for, jsonify, 
                   session,Blueprint)
from client.model.users import Client, db
import os

# Define paths based on your project structure
template_folder = os.path.join(os.path.dirname(__file__), '../templates')
static_folder = os.path.join(os.path.dirname(__file__), '../static')

# Create Blueprint with adjusted paths
auth_admin = Blueprint(
    'auth_admin', __name__,
    static_folder=static_folder,  # Points to /home/adam/Desktop/vet/app/admin/static
    template_folder=template_folder  # Points to /home/adam/Desktop/vet/app/admin/templates
)

@auth_admin.route('/login-admin', methods=['GET'])
def show_login_admin():
    return render_template('admin-login.html')

# Process the login form submission (POST request)
@auth_admin.route('/login-admin', methods=['POST'])
def login_admin():
    # Process login form data here (e.g., check username and password)
    username = request.form.get('username')
    password = request.form.get('password')
    # Query database to check if a user exists with this username or email
    user = Client.query.filter((Client.email == username_or_email) | (Client.uname == username_or_email)).first()
    
    if not user or not user.check_password(password):
        # Return JSON error message for invalid credentials
        return jsonify({'message': 'Invalid username/email or password.'}), 404
      
    # If login is successful, set session or return success message
    # If login is successful, set session data
    session['user_id'] = user.client_id  # Store the user ID in the session
    session['username'] = user.uname  # Store the username in the session
    return jsonify({'message': 'Login successful!', 'redirect': url_for('dashboard_admin.admin-dashboard')}), 200
    
