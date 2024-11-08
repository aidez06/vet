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
