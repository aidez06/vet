-- Create client table
CREATE TABLE client (
    client_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,  -- Unique constraint on email
    contact_num VARCHAR(20),
    uname VARCHAR(50) NOT NULL UNIQUE,  -- Unique constraint on username
    pword VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create pet table
CREATE TABLE pet (
    pet_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    age INTEGER,
    breed VARCHAR(100),
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE CASCADE,
    UNIQUE (client_id, name)  -- Composite unique constraint to prevent duplicate pet names for the same client
);

-- Create service table
CREATE TABLE service (
    service_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,  -- Unique constraint on service name (optional)
    description TEXT,
    price NUMERIC(10, 2)
);

-- Create appoint table
CREATE TABLE appoint (
    appoint_id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    pet_id INTEGER NOT NULL,
    service_id INTEGER,
    appointment_date TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE CASCADE,
    FOREIGN KEY (pet_id) REFERENCES pet(pet_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES service(service_id) ON DELETE SET NULL
);
