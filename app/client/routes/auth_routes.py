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
    # Get form data
    username_or_email = request.form.get('username_or_email')
    password = request.form.get('password')

    # Query database to check if a user exists with this username or email
    user = Client.query.filter((Client.email == username_or_email) | (Client.uname == username_or_email)).first()

    if not user:
        # If no user is found, return an error message
        return jsonify({'message': 'Invalid username/email or password.'}), 404

    # Check if the password matches
    if not user.check_password(password):
        # If password does not match, return an error message
        return jsonify({'message': 'Invalid username/email or password.'}), 404

    # If login is successful, set session or return success message
    session['user_id'] = user.client_id  # Optional: Set a session for the user
    return redirect(url_for('public.booking'))  # Replace 'booking_page' with the actual route for your booking page


@auth.route('/register', methods=['POST'])
def register():
    # Get form data with updated names matching the placeholders in your HTML
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    username = request.form.get('uname')
    password = request.form.get('pword')
    contact_num = request.form.get('contact_num')

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
    new_client.set_password(password)  # Hashes and sets the password

    # Save the client to the database
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'message': 'Registration successful! Please log in.'}), 200