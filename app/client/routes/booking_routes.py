from flask import (request, redirect, url_for, jsonify, session, Blueprint)
from client.model.users import Appoint, Pet, Service, Client, db
from datetime import datetime
import os

template_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
book = Blueprint('book', __name__, static_folder=static_folder, template_folder=template_folder)

@book.route('/book_appointment', methods=['POST'])
def book_appointment():
    # Retrieve client_id from the session
    client_id = session.get('user_id')
    if not client_id:
        return jsonify({"status": "error", "message": "User not logged in"}), 401

    # Parse JSON data from the request
    data = request.get_json()
    pet_name = data.get('pet_name')
    pet_gender = data.get('pet_gender')
    pet_type = data.get('pet_type')
    breed = data.get('breed')
    pet_age = data.get('pet_age')
    pet_service = data.get('pet_service')
    custom_service = data.get('custom_service')
    appointment_date = data.get('appointment_date')
    appointment_time = data.get('appointment_time')
    notes = data.get('notes')
    status = "Scheduled"  # Default status for new appointments

    # Debugging: Log values to ensure they’re not None
    print("Pet Name:", pet_name)
    print("Pet Gender:", pet_gender)
    print("Pet Type:", pet_type)
    print("Breed:", breed)
    print("Pet Age:", pet_age)

    # Check for required fields (like pet_name) before proceeding
    if not pet_name or not pet_type:
        return jsonify({"status": "error", "message": "Pet name and type are required fields."}), 400

    # Step 1: Register the Pet
    try:
        pet_id = register_pet(client_id, pet_name, pet_type, pet_age, breed, pet_gender)
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    # Step 2: Create the Appointment
    try:
        # Add custom service description to notes if specified
        if custom_service:
            notes = (notes or "") + f" (Custom Service: {custom_service})"
        
        # Book the appointment
        appoint_id = create_appointment(
            client_id=client_id,
            pet_id=pet_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status=status,
            service_name=pet_service,
            custom_service_description=custom_service
        )
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    # Step 3: Return Success Response
    return jsonify({"status": "success", "message": "Appointment booked successfully!", "appoint_id": appoint_id})

def register_pet(client_id, name, pet_type, age, breed, gender):
    # Check if the client exists
    client = Client.query.get(client_id)
    if not client:
        raise ValueError("Client does not exist")

    # Create new pet
    new_pet = Pet(
        client_id=client_id,
        name=name,
        type=pet_type,
        age=age,
        breed=breed,
        gender=gender
    )

    # Add and commit to the database
    db.session.add(new_pet)
    db.session.commit()

    print("New pet registered with pet_id:", new_pet.pet_id)
    return new_pet.pet_id  # Return the auto-generated pet_id

def create_appointment(client_id, pet_id, appointment_date, appointment_time, status, service_name=None, custom_service_description=None):
    # Validate client and pet
    client = Client.query.get(client_id)
    pet = Pet.query.get(pet_id)
    if not client or not pet:
        raise ValueError("Client or Pet does not exist")

    # Convert appointment date and time to datetime object
    try:
        appointment_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Invalid date or time format")

    # Fetch or create the service
    service_id = None
    if service_name:
        service = Service.query.filter_by(name=service_name).first()
        if not service and custom_service_description:
            # Create a new service if not found and custom description provided
            new_service = Service(name=service_name, description=custom_service_description)
            db.session.add(new_service)
            db.session.commit()  # Commit to get the new service_id
            service_id = new_service.service_id
        elif service:
            service_id = service.service_id

    # Create new appointment
    new_appointment = Appoint(
        client_id=client_id,
        pet_id=pet_id,
        service_id=service_id,
        appointment_date=appointment_datetime,
        status=status,
        notes=custom_service_description or ""  # Add custom description to notes if applicable
    )

    # Add and commit the appointment
    db.session.add(new_appointment)
    db.session.commit()

    print("New appointment created with appoint_id:", new_appointment.appoint_id)
    return new_appointment.appoint_id  # Return the auto-generated appoint_id
