document.addEventListener('DOMContentLoaded', function() {
    // Handle progress bars
    const progressFills = document.querySelectorAll('.progress-fill[data-progress]');
    progressFills.forEach(fill => {
        const progress = fill.getAttribute('data-progress');
        fill.style.setProperty('--progress-width', progress + '%');
    });
}); 