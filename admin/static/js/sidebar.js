
const sidebar = document.getElementById('sidebar');
const content = document.getElementById('content');
const toggleSidebar = document.getElementById('toggleSidebar');

toggleSidebar.addEventListener('click', () => {
    const isMinimized = sidebar.classList.toggle('minimized');
    content.classList.toggle('minimized');

    // Update the position of the toggle button based on sidebar state
    toggleSidebar.style.left = isMinimized ? '90px' : '210px';
});
