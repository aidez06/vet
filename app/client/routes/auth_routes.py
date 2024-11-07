from flask import (request, redirect, 
                   url_for, jsonify, 
                   session,Blueprint)
from client.model.users import Client, db
import os


template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
auth = Blueprint('auth', __name__,static_folder=static_folder, template_folder=template_folder)



@auth.route('/login', methods=['POST'])
def login():

    username_or_email = request.form.get('usernameLogin')
    password = request.form.get('pwdLogin')
    # Query database to check if a user exists with this username or email
    user = Client.query.filter((Client.email == username_or_email) | (Client.uname == username_or_email)).first()
    
    if not user or not user.check_password(password):
        # Return JSON error message for invalid credentials
        return jsonify({'message': 'Invalid username/email or password.'}), 404
    # If login is successful, set session or return success message
        # If login is successful, set session data
    session['user_id'] = user.client_id  # Store the user ID in the session
    session['username'] = user.uname  # Store the username in the session
    return jsonify({'message': 'Login successful!', 'redirect': url_for('public.booking')}), 200



@auth.route('/register', methods=['POST'])
def register():
    # Get form data with updated names matching the placeholders in your HTML
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    username = request.form.get('uname')
    password = request.form.get('pword')
    contact_num = request.form.get('contact_num')
    print(password, username)
    # Check if username or email already exists
    existing_user = Client.query.filter((Client.email == email) | (Client.uname == username)).first()
    if existing_user:
        if existing_user.email == email:
            return jsonify({'message': 'This email is already in use.'}), 404
        if existing_user.uname == username:
            return jsonify({'message': 'This username is already in use.'}), 404

    # Create a new client and hash the password
    new_client = Client(
        first_name=first_name,
        last_name=last_name,
        email=email,
        contact_num=contact_num,
        uname=username
    )
    
    encrpt_password = new_client.set_password(password)  # Hashes and sets the password
    print(encrpt_password)
    # Save the client to the database
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'message': 'Registration successful! Please log in.'}), 200
@auth.route('/logout')
def logout():
    session.clear()  # Clears all session data
    return redirect(url_for('public.home'))
