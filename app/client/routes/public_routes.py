from flask import Blueprint,render_template, url_for,render_template_string
import os

template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

public = Blueprint('public', __name__, static_folder=static_folder, template_folder=template_folder)

@public.route('/home')
def home():
    return render_template('/public/home.html')

@public.route('/about')
def about():
    return render_template('/public/about.html')

