INSERT INTO client (first_name, last_name, email, contact_num, uname, pword)
VALUES 
('John', 'Doe', 'johndoe@gmail.com', '09123456789', 'john_doe', 'password123'),
('Jane', 'Smith', 'janesmith@gmail.com', '09129876543', 'jane_smith', 'password456');

INSERT INTO pet (client_id, name, type, age, breed, gender)
VALUES 
(1, 'Buddy', 'Dog', 3, 'Golden Retriever', 'Male'),
(1, 'Mittens', 'Cat', 2, 'Siamese', 'Female'),
(2, 'Charlie', 'Dog', 1, 'Labrador', 'Male');

INSERT INTO service (name, description, price)
VALUES 
('General Check-up', 'Routine health check-up for pets.', 500.00),
('Vaccination', 'Vaccination for dogs and cats.', 300.00),
('Grooming', 'Full grooming service for pets.', 700.00);

INSERT INTO appoint (client_id, pet_id, service_id, custom_service, appoint_date, status, notes)
VALUES 
(1, 1, 1, NULL, '2024-11-10 10:00:00', 'Scheduled', 'Bring vaccination records.'),
(1, 2, NULL, 'Dental cleaning', '2024-11-12 14:00:00', 'Scheduled', 'Check for tartar.'),
(2, 3, 2, NULL, '2024-11-15 09:00:00', 'Scheduled', 'First vaccination.');
