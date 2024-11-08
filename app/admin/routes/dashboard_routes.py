from flask import (request, render_template, 
                   url_for, jsonify, 
                   redirect,Blueprint)
from client.model.users import Client,Appoint, Service,Pet, db
from datetime import datetime

import os


template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')

# Create Blueprint with adjusted paths
dashboard_admin = Blueprint(
    'dashboard_admin', __name__,
    static_folder=static_folder,  
    template_folder=template_folder 
)
@dashboard_admin.route('/add-product')
def add_product():
    return render_template('admin-add-product.html')
@dashboard_admin.route('/products')
def products():
    return render_template('admin-product-table.html')
@dashboard_admin.route('/manage-appointment')
def manage_appointment():
    appointments = Appoint.query.join(Client).join(Pet).all()
    return render_template('manage-appointment.html', appointments=appointments)

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
@dashboard_admin.route('/admin/get-appointment/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment = Appoint.query.get(appointment_id)
    if not appointment:
        return jsonify({"status": "error", "message": "Appointment not found"}), 404

    client = appointment.client
    pet = appointment.pet
    service = appointment.service

    appointment_data = {
        "appoint_id": appointment.appoint_id,
        "client_name": f"{client.first_name} {client.last_name}" if client else "Unknown",
        "status": appointment.status,
        "pet_name": pet.name if pet else "Unknown",
        "service_name": service.name if service else "Custom Service",
        "appointment_datetime": appointment.appointment_date.strftime('%Y-%m-%dT%H:%M'),
        "contact_number": client.contact_num if client else "Unknown"
    }

    return jsonify({"status": "success", "data": appointment_data}), 200
@dashboard_admin.route('/update-appointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    # Retrieve the data sent in the request body
    data = request.get_json()

    # Fetch the appointment by ID
    appointment = Appoint.query.get(appointment_id)
    if not appointment:
        return jsonify({"status": "error", "message": "Appointment not found"}), 404

    try:
        # Update the fields with the new data
        appointment.status = data.get('status', appointment.status)

        # Update client details if they are editable
        client = appointment.client
        if client:
            client.first_name, client.last_name = data.get('client_name', '').split(' ', 1)
            client.contact_num = data.get('contact_number', client.contact_num)

        # Update pet details if they are editable
        pet = appointment.pet
        if pet:
            pet.name = data.get('pet_name', pet.name)

        # Update service details if applicable
        service = Service.query.filter_by(name=data.get('service_name')).first()
        if service:
            appointment.service_id = service.service_id
        elif data.get('service_name'):  # If a custom service is provided
            new_service = Service(name=data.get('service_name'), description="Custom Service")
            db.session.add(new_service)
            db.session.flush()  # Get the new service ID
            appointment.service_id = new_service.service_id

        # Update appointment date and time
        appointment.appointment_date = datetime.strptime(
            data.get('appointment_datetime', appointment.appointment_date.strftime('%Y-%m-%dT%H:%M')),
            '%Y-%m-%dT%H:%M'
        )

        # Commit all changes to the database
        db.session.commit()

        return jsonify({"status": "success", "message": "Appointment updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()  # Rollback the transaction if there’s an error
        return jsonify({"status": "error", "message": str(e)}), 500
@dashboard_admin.route('/delete-appointment/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    # Fetch the appointment
    appointment = Appoint.query.get(appointment_id)
    if not appointment:
        return jsonify({"status": "error", "message": "Appointment not found"}), 404

    try:
        # Delete the appointment
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"status": "success", "message": "Appointment deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of an error
        return jsonify({"status": "error", "message": str(e)}), 500
