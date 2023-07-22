// static/main.js
document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.getElementById('sidebar-toggle');

    // Function to toggle the visibility of the sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('visible');
    }

    toggleButton.addEventListener('click', toggleSidebar);
});
