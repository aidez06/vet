document.addEventListener("DOMContentLoaded", function () {
    const signupForm = document.getElementById("signupForm");
    const loginForm = document.getElementById("loginForm");
    const welcomeText = document.getElementById("welcomeText");
    const welcomeSection = document.querySelector(".welcome-section");
    const formSection = document.querySelector(".form-section");

    // Show login form
    document.getElementById("toggleToLogin").addEventListener("click", function () {
        if (!loginForm.classList.contains("d-none")) {
            return; 
        }
        
        // Slide the welcome section out to the right
        welcomeSection.classList.add("slide-out");

        setTimeout(() => {
            signupForm.classList.add("d-none"); // Hide the signup form
            loginForm.classList.remove("d-none"); // Show the login form
            welcomeText.textContent = "Welcome Back!";
            formSection.classList.remove("slide-out");
            formSection.classList.add("slide-in"); 
        }, 600); 
    });

    // Show signup form
    document.getElementById("toggleToSignup").addEventListener("click", function () {
        if (!signupForm.classList.contains("d-none")) {
            return;
        }

        // Slide the welcome section back in
        welcomeSection.classList.add("slide-in"); // Slide back in

        // Show the signup form after sliding back in
        setTimeout(() => {
            loginForm.classList.add("d-none"); // Hide the login form
            signupForm.classList.remove("d-none"); 
            welcomeText.textContent = "Welcome";
        }, 600); 
    });
});
