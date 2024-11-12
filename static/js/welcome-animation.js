window.onload = function() {
    const starCount = 100;  // Number of stars
    const starContainer = document.querySelector('.stars');
    const mainContent = document.getElementById('main-content');
    const welcomeOverlay = document.getElementById('welcome-overlay');

    // Function to create stars
    function createStars() {
        for (let i = 0; i < starCount; i++) {
            const star = document.createElement('div');
            star.classList.add('star');
            const size = Math.random() * 3 + 2;  // Random size for stars
            star.style.width = `${size}px`;
            star.style.height = `${size}px`;
            star.style.left = `${Math.random() * 100}vw`;  // Random horizontal position
            star.style.top = `${Math.random() * 100}vh`;   // Random vertical position
            star.style.animationDelay = `${Math.random() * 2}s`;  // Random delay for star appearance
            starContainer.appendChild(star);
        }
    }

    // Trigger the star creation
    createStars();

    // Remove the welcome screen after the animation
    setTimeout(function() {
        welcomeOverlay.style.display = 'none';  // Hide the overlay
        mainContent.classList.add('fade-in');   // Show the main content
    }, 4000);  // Animation duration (4 seconds)
};
