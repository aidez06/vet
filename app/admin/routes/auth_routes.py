from flask import (request, render_template, 
                   url_for, jsonify, redirect, 
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
    username = request.form.get('email')
    password = request.form.get('password')
    print('Starting...')
    print(username, password)
    
    # Example: Query the Client model to authenticate
    client = Client.query.filter_by(email=username).first()
    
    if client and client.check_password(password):  # Assume check_password method exists
        # Set session or other login state here
        session['admin_logged_in'] = True
        return redirect(url_for('admin.admin-pos'))  # Redirect to admin dashboard or other page
    
    # If login fails, redirect back to login page or show error
    return render_template('admin-login.html', error="Invalid credentials")