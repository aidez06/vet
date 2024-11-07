const sidebar = document.getElementById('sidebar');
const content = document.getElementById('content');
const toggleSidebar = document.getElementById('toggleSidebar');

toggleSidebar.addEventListener('click', () => {
    const isMinimized = sidebar.classList.toggle('minimized');
    content.classList.toggle('minimized');

    // Update the position of the toggle button based on sidebar state
    toggleSidebar.style.left = isMinimized ? '90px' : '210px';
});


// Vet Clinic Data
var xValues = ["Dogs", "Cats", "Birds", "Reptiles", "Others"];
var yValues = [55, 35, 5, 3, 2]; // 
var barColors = [
    "#b91d47",
    "#59D5E0",
    "#2b5797",
    "#e8c3b9",
    "#1e7145"
];

new Chart("myChart", {
    type: "doughnut",
    data: {
        labels: xValues,
        datasets: [{
            backgroundColor: barColors,
            data: yValues,
            borderWidth: 0 
        }]
    },
    options: {
        plugins: {
            legend: {
                display: true,
                labels: {
                    color: '#FFFFFF', // Set legend text color to white
                    font: {
                        size: 14, // Set the font size
                        family: 'Arial', 
                    }
                }
            },
            tooltip: {
                titleColor: '#FFFFFF', 
                bodyColor: '#FFFFFF' 
            }
        },
        cutout: '50%', // Adjust for doughnut chart appearance
        elements: {
            arc: {
                borderWidth: 0 
            }
        },
        responsive: true, 
        maintainAspectRatio: false 
    }
});