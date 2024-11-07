from flask import request, jsonify, session, Blueprint
from client.model.users import Client, Pet, Service, Appoint, db
from datetime import datetime
import os


template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
auth = Blueprint('auth', __name__,static_folder=static_folder, template_folder=template_folder)

# Book appointment route
@auth.route('/book-appointment', methods=['POST'])
def book_appointment():
    client_id = session.get('user_id')
    if not client_id:
        return jsonify({'error': 'User not logged in.'}), 403

    # Retrieve form data
    pet_gender = request.form.get('pet_gender')
    pet_service = request.form.get('pet_service')
    pet_name = request.form.get('pet_name')
    custom_service = request.form.get('custom_service')
    pet_type = request.form.get('pet_type')
    appointment_date = request.form.get('appointment_date')
    appointment_time = request.form.get('appointment_time')
    breed = request.form.get('breed')
    pet_age = request.form.get('pet_age')
    notes = request.form.get('notes')

    # Check for or create pet
    pet = Pet.query.filter_by(client_id=client_id, name=pet_name).first()
    if not pet:
        pet = Pet(
            client_id=client_id,
            name=pet_name,
            type=pet_type,
            age=pet_age,
            breed=breed,
            gender=pet_gender
        )
        db.session.add(pet)
        db.session.commit()

    # Check for or create service
    service = Service.query.filter_by(name=pet_service).first()
    if not service and custom_service:
        service = Service(name=custom_service, description=notes)
        db.session.add(service)
        db.session.commit()

    # Parse date and time for appointment
    appointment_datetime = f"{appointment_date} {appointment_time}"
    try:
        appointment_datetime = datetime.strptime(appointment_datetime, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid date or time format.'}), 400

    # Create appointment
    appointment = Appoint(
        client_id=client_id,
        pet_id=pet.pet_id,
        service_id=service.service_id,
        appointment_date=appointment_datetime,
        status='Scheduled'
    )

    db.session.add(appointment)
    db.session.commit()

    return jsonify({'message': 'Appointment booked successfully!'}), 200
