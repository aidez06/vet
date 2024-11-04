from datetime import datetime, timezone
from utils.database_connection import db
class Client(db.Model):
    __tablename__ = 'client'

    client_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    contact_num = db.Column(db.String(20))
    uname = db.Column(db.String(50), nullable=False)
    pword = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to pets
    pets = db.relationship('Pet', backref='owner', cascade="all, delete", lazy=True)
    appointments = db.relationship('Appoint', backref='client', lazy=True)

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
