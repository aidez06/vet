const welcomeContainer = document.querySelector(".welcome-container");
const toggleToSignup = document.getElementById("toggleToSignup");
const toggleToLogin = document.getElementById("toggleToLogin");

// togglesignup
toggleToSignup.addEventListener("click", function(event) {
    event.preventDefault();
    welcomeContainer.classList.add("slide-in");
    welcomeContainer.classList.remove("slide-out");
});

// togglesignin
toggleToLogin.addEventListener("click", function(event) {
    event.preventDefault();
    welcomeContainer.classList.add("slide-out");
    welcomeContainer.classList.remove("slide-in");
});
