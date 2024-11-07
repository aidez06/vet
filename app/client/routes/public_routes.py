from flask import Blueprint,render_template, url_for,session,redirect
import os

template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

public = Blueprint('public', __name__, static_folder=static_folder, template_folder=template_folder)

@public.route('/home')
def home():
            # Check if the user is already logged in
    if 'user_id' in session:
        # Redirect to the booking page or any other page if already logged in
        return redirect(url_for('public.booking'))
    # Get form data
    return render_template('/public/home.html')

@public.route('/about')
def about():
    return render_template('/public/about.html')
@public.route('/contact')
def contact():
    return render_template('/public/contact.html')
@public.route('/service')
def service():
    return render_template('/public/service.html')

@public.route('/booking')
def booking():
    username = session.get('username')
    print("Username from session:", username)  # Debugging print statement
    
    if not username:
        return redirect(url_for('public.home'))

    return render_template('public/booking.html', username=username)




