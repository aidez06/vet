from datetime import datetime, timezone
from client.utils.database_connection import db
from werkzeug.security import generate_password_hash, check_password_hash

class Client(db.Model):
    __tablename__ = 'client'

    client_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True) 
    contact_num = db.Column(db.String(20))
    uname = db.Column(db.String(50), nullable=False, unique=True)  # Ensure uniqueness
    pword = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationship to pets and appointments
    pets = db.relationship('Pet', backref='owner', cascade="all, delete", lazy=True)
    appointments = db.relationship('Appoint', backref='client', lazy=True)

    def set_password(self, password):
        print("Password input:", password)

        if password is not None:
            self.pword = generate_password_hash(password)
            print(self.pword)
        else:
            raise ValueError("Password cannot be None")

    def check_password(self, password):
        print("Stored hash:", self.pword)
        print("Password input:", password)
        validate_password = check_password_hash(self.pword, password)
        print(validate_password)
        return validate_password

class Pet(db.Model):
    __tablename__ = 'pet'

    pet_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    age = db.Column(db.Integer)
    breed = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationship to appointments
    appointments = db.relationship('Appoint', backref='pet', lazy=True)

class Service(db.Model):
    __tablename__ = 'service'

    service_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))

    # Relationship to appointments
    appointments = db.relationship('Appoint', backref='service', lazy=True)

class Appoint(db.Model):
    __tablename__ = 'appoint'

    appoint_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id', ondelete="CASCADE"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.pet_id', ondelete="CASCADE"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id', ondelete="SET NULL"), nullable=True)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    notes = db.Column(db.Text)  # Add this line to include a notes column
