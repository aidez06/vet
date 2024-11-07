from flask import (request, render_template, 
                   url_for, jsonify, 
                   redirect,Blueprint)
from client.model.users import Client,Appoint, Service,db
import os


template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

# Create Blueprint with adjusted paths
dashboard_admin = Blueprint(
    'dashboard_admin', __name__,
    static_folder=static_folder,  
    template_folder=template_folder 
)


@dashboard_admin.route('/appointments')
def appointments():
    # Query appointments, joining related tables for full details
    appointment_data = db.session.query(
        Appoint, Client, Service
    ).join(Client, Appoint.client_id == Client.client_id)\
     .join(Service, Appoint.service_id == Service.service_id)\
     .all()
    print(appointment_data)
    # Pass the data to the template
    return render_template('admin-dashboard.html', appointments=appointment_data)