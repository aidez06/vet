// Appoinment Calendar
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: [
            { title: 'Appointment 1', start: '2024-11-05T10:00:00' }, // 10:00 AM on November 5, 2024
            { title: 'Appointment 2', start: '2024-11-07T14:30:00' }, // 2:30 PM on November 7, 2024
            { title: 'Appointment 3', start: '2024-11-07T16:00:00' }  // 4:00 PM on November 7, 2024
        ],
        eventTimeFormat: { // 12-hour format with AM/PM
            hour: 'numeric',
            minute: '2-digit',
            meridiem: 'short' // To show AM/PM
        },
        eventContent: function(arg) {
            // Event rendering showing title and time
            let timeText = arg.timeText ? `${arg.timeText}` : '';
            let titleText = `<div class="fc-event-title">${arg.event.title}</div>`;
            return { html: `${timeText} ${titleText}` };
        }
    });
    calendar.render();
});

document.addEventListener('DOMContentLoaded', () => {
    let selectedAppointmentId = null; // Store the selected appointment ID

    // Event delegation to handle clicks on edit buttons
    document.getElementById('appointmentTable').addEventListener('click', function (event) {
        const editButton = event.target.closest('.edit-btn'); // Ensure the clicked button is an edit button
        if (editButton) {
            // Get the appointment ID from the clicked button's data attribute
            selectedAppointmentId = editButton.dataset.appointmentId;
            console.log('Selected Appointment ID:', selectedAppointmentId);

            // Retrieve row data from the closest table row
            const row = editButton.closest('tr'); // Get the parent row of the clicked button
            const clientName = row.getAttribute('data-client-name');
            const status = row.getAttribute('data-status');
            const pet = row.getAttribute('data-pet');
            const service = row.getAttribute('data-service');
            const date = row.getAttribute('data-date');
            const contact = row.getAttribute('data-contact');

            console.log({
                clientName,
                status,
                pet,
                service,
                date,
                contact
            });

            // Populate the modal fields with the row's data
            document.getElementById('updateAppointmentId').value = selectedAppointmentId;
            document.getElementById('updateClientName').value = clientName || '';
            document.getElementById('updateStatus').value = status || '';
            document.getElementById('updatePet').value = pet || '';
            document.getElementById('updateService').value = service || '';
            document.getElementById('updateDateTime').value = date || '';
            document.getElementById('updateContactNumber').value = contact || '';

            // Show the update modal
            new bootstrap.Modal(document.getElementById('updateModal')).show();
        }
    });

    // Save changes button functionality
    document.getElementById('saveUpdateButton').addEventListener('click', function () {
        if (!selectedAppointmentId) {
            console.error('No appointment ID selected for update');
            return;
        }

        // Collect updated data from the modal form
        const updatedData = {
            client_name: document.getElementById('updateClientName').value,
            status: document.getElementById('updateStatus').value,
            pet_name: document.getElementById('updatePet').value,
            service_name: document.getElementById('updateService').value,
            appointment_datetime: document.getElementById('updateDateTime').value,
            contact_number: document.getElementById('updateContactNumber').value
        };

        console.log(`Sending PUT request to: /admin/update-appointment/${selectedAppointmentId}`);
        console.log('Updated Data:', JSON.stringify(updatedData));

        // Send the updated data to the server
        console.log(selectedAppointmentId);s
        fetch(`/admin/update-appointment/${selectedAppointmentId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        })
            .then(response => {
                if (response.ok) {
                    console.log('Appointment updated successfully');
                    location.reload(); // Reload the page or dynamically update the table
                } else {
                    console.error('Failed to update appointment:', response.status);
                }
            })
            .catch(error => {
                console.error('Error occurred while updating:', error);
            });
    });
});
    // Event listener for delete button
    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', function() {
            const appointmentId = this.dataset.appointmentId; // Set data attributes
            document.getElementById('deleteAppointmentId').value = appointmentId;
            new bootstrap.Modal(document.getElementById('deleteModal')).show();
        });
    });

    document.addEventListener('DOMContentLoaded', () => {
        let selectedAppointmentId = null; // Variable to store the selected appointment ID
    
        // Event delegation for delete buttons
        document.getElementById('appointmentTable').addEventListener('click', function (event) {
            const deleteButton = event.target.closest('.delete-btn');
            if (deleteButton) {
                const appointmentId = deleteButton.getAttribute('data-appointment-id');
                console.log(`Deleting appointment with ID: ${appointmentId}`); // Debugging log
    
                // Check if appointmentId is found
                if (appointmentId) {
                    // Store the appointment ID in the variable
                    selectedAppointmentId = appointmentId;
    
                    // Show the delete confirmation modal
                    new bootstrap.Modal(document.getElementById('deleteModal')).show();
                } else {
                    console.error('Appointment ID not found.');
                }
            }
        });
    
        // Confirm delete button functionality
        document.getElementById('confirmDeleteButton').addEventListener('click', function () {
            console.log(`Confirming delete for appointment ID: ${selectedAppointmentId}`); // Debugging log
    
            // Ensure the ID is set before making the delete request
            if (!selectedAppointmentId) {
                console.error('Appointment ID is undefined');
                return; // Early exit if ID is not set
            }
    
            // Make the DELETE request
            fetch(`/admin/delete-appointment/${selectedAppointmentId}`, {
                method: 'DELETE'
            })
                .then(response => {
                    if (response.ok) {
                        console.log('Appointment deleted successfully.');
                        location.reload(); // Reload the page or update the UI
                    } else {
                        console.error('Failed to delete appointment:', response.status);
                    }
                })
                .catch(error => {
                    console.error('Error occurred:', error);
                });
        });
    });

    

       // Function to filter the table
       function filterTable() {
        const clientSearch = document.getElementById('clientSearch').value.toLowerCase();
        const statusFilter = document.getElementById('statusFilter').value;
        const petFilter = document.getElementById('petFilter').value;
        const serviceSearch = document.getElementById('serviceSearch').value.toLowerCase();
        const dateSearch = document.getElementById('dateSearch').value.toLowerCase();
        const contactSearch = document.getElementById('contactSearch').value.toLowerCase();
        const rows = document.querySelectorAll('#appointmentTable tbody tr');

        rows.forEach(row => {
            const clientName = row.getAttribute('data-client-name').toLowerCase();
            const status = row.getAttribute('data-status');
            const pet = row.getAttribute('data-pet').toLowerCase();
            const service = row.getAttribute('data-service').toLowerCase();
            const date = row.getAttribute('data-date').toLowerCase();
            const contact = row.getAttribute('data-contact').toLowerCase();

            const matchesClient = clientName.includes(clientSearch);
            const matchesStatus = (statusFilter === 'All' || status === statusFilter);
            const matchesPet = (petFilter === 'All' || pet === petFilter);
            const matchesService = service.includes(serviceSearch);
            const matchesDate = date.includes(dateSearch);
            const matchesContact = contact.includes(contactSearch);

            // Show or hide the row based on the search criteria
            if (matchesClient && matchesStatus && matchesPet && matchesService && matchesDate && matchesContact) {
                row.style.display = ''; // Show row
            } else {
                row.style.display = 'none'; // Hide row
            }
        });
    }

    // Add event listeners for search inputs and select elements
    document.getElementById('clientSearch').addEventListener('keyup', filterTable);
    document.getElementById('statusFilter').addEventListener('change', filterTable);
    document.getElementById('petFilter').addEventListener('change', filterTable);
    document.getElementById('serviceSearch').addEventListener('keyup', filterTable);
    document.getElementById('dateSearch').addEventListener('keyup', filterTable);
    document.getElementById('contactSearch').addEventListener('keyup', filterTable);
