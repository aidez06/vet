from flask import Blueprint, render_template
import os

template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
auth = Blueprint('auth', __name__,static_folder=static_folder, template_folder=template_folder)


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/register')
def register():
    return render_template('auth/registration.html')