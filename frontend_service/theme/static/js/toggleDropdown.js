"use strict";
document.addEventListener('DOMContentLoaded', () => {
    const dropdownButton = document.getElementById('dropdownButton');
    const dropdownMenu = document.getElementById('dropdownMenu');
    if (dropdownButton && dropdownMenu) {
        dropdownButton.addEventListener('click', () => {
            dropdownMenu.classList.toggle('hidden');
        });
        // Optional: Close the dropdown when clicking outside
        document.addEventListener('click', (event) => {
            if (dropdownMenu.classList.contains('hidden') === false &&
                !dropdownButton.contains(event.target) &&
                !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.add('hidden');
            }
        });
    }
});
