from flask import Flask, request, render_template, redirect, flash, url_for
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def get_db_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return connection

# Route for adding a client
@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        contact_num = request.form['contact_num']
        uname = request.form['uname']
        pword = request.form['pword']

        if not (first_name and last_name and uname and pword):
            flash('Missing required fields.', 'error')
            return redirect(url_for('add_client'))

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO client (first_name, last_name, email, contact_num, uname, pword)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (first_name, last_name, email, contact_num, uname, pword))
            conn.commit()
            flash('Client added successfully!', 'success')
            return redirect(url_for('add_client'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        finally:
            cur.close()
            conn.close()

    return render_template('add_client.html') # Change the html file


# Route for adding a pet
@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        client_id = request.form['client_id']
        name = request.form['name']
        pet_type = request.form['type']
        age = request.form['age']
        breed = request.form['breed']
        gender = request.form['gender']

        if not (client_id and name):
            flash('Missing required fields.', 'error')
            return redirect(url_for('add_pet'))

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO pet (client_id, name, type, age, breed, gender)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (client_id, name, pet_type, age, breed, gender))
            conn.commit()
            flash('Pet added successfully!', 'success')
            return redirect(url_for('add_pet'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        finally:
            cur.close()
            conn.close()

    return render_template('add_pet.html') # Change the html file


# Route for adding a service
@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        if not (name and price):
            flash('Missing required fields.', 'error')
            return redirect(url_for('add_service'))

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO service (name, description, price)
                VALUES (%s, %s, %s)
            ''', (name, description, price))
            conn.commit()
            flash('Service added successfully!', 'success')
            return redirect(url_for('add_service'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        finally:
            cur.close()
            conn.close()

    return render_template('add_service.html') # Change the html file


# Route for adding an appointment
@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        client_id = request.form['client_id']
        pet_id = request.form['pet_id']
        service_id = request.form['service_id']
        custom_service = request.form['custom_service']
        appoint_date = request.form['appoint_date']
        notes = request.form['notes']

        if not (appoint_date and (service_id or custom_service)):
            flash('Missing required fields.', 'error')
            return redirect(url_for('add_appointment'))

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO appoint (client_id, pet_id, service_id, custom_service, appoint_date, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (client_id, pet_id, service_id, custom_service, appoint_date, notes))
            conn.commit()
            flash('Appointment added successfully!', 'success')
            return redirect(url_for('add_appointment'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        finally:
            cur.close()
            conn.close()

    return render_template('add_appointment.html') # Change the html file


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
