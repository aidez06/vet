-- Create client table
CREATE TABLE client (
    client_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    contact_num VARCHAR(20),
    uname VARCHAR(50) NOT NULL,
    pword VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create pet table, linking each pet to a client
CREATE TABLE pet (
    pet_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES client(client_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    age INT,
    breed VARCHAR(100),
    gender VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create service table for different types of veterinary services
CREATE TABLE service (
    service_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,  -- e.g., "General Check-up"
    description TEXT,
    price NUMERIC(10, 2)         -- Cost of the service
);

-- Modify the appoint table to add a custom_service field
CREATE TABLE appoint (
    appoint_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES client(client_id) ON DELETE SET NULL,
    pet_id INT REFERENCES pet(pet_id) ON DELETE SET NULL,
    service_id INT REFERENCES service(service_id) ON DELETE SET NULL,
    custom_service VARCHAR(100),  -- Allows entry of a custom service if service_id is NULL
    appoint_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'Scheduled',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (service_id IS NOT NULL AND custom_service IS NULL) OR 
        (service_id IS NULL AND custom_service IS NOT NULL)
    )
);
