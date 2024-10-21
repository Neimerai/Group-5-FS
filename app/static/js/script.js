    // Function to show the Sign-Up pop-up when clicking the Log In button
    function openSignUp() {
        const signUpPopup = document.getElementById('registerPopup');
        signUpPopup.classList.remove('hidden');
    }
    
    // Function to show the Sign-Up pop-up and hide the Login pop-up
    function showSignUp() {
        const loginPopup = document.getElementById('loginPopup');
        const signUpPopup = document.getElementById('registerPopup');
        
        loginPopup.classList.add('hidden');
        signUpPopup.classList.remove('hidden');
    }
    
    // Function to show the Login pop-up and hide the Sign-Up pop-up
    function showLogin() {
        const loginPopup = document.getElementById('loginPopup');
        const signUpPopup = document.getElementById('registerPopup');
        
        signUpPopup.classList.add('hidden');
        loginPopup.classList.remove('hidden');
    }
    
    // Function to close the current pop-up
    function closePopup(popupId) {
        const popup = document.getElementById(popupId);
        popup.classList.add('hidden');
    }

    document.addEventListener('DOMContentLoaded', () => {
        // Attach event listeners for form submissions
    
        // Sign-Up Form
        const registerForm = document.querySelector('#registerPopup form');
        if (registerForm) {
            registerForm.addEventListener('submit', function(event) {
                event.preventDefault(); // Prevent form submission to server
    
                // Get user input
                const newUser = {
                    firstName: document.getElementById('first-name').value,
                    lastName: document.getElementById('last-name').value,
                    email: document.getElementById('sign-up-email').value,
                    phone: document.getElementById('phone').value,
                    password: document.getElementById('sign-up-password').value
                };
    
                // Call registerUser() from mock backend
                if (registerUser(newUser)) {
                    showLogin();
                }
            });
        }
    
        // Login Form
        const loginForm = document.querySelector('#loginPopup form');
        if (loginForm) {
            loginForm.addEventListener('submit', function(event) {
                event.preventDefault(); // Prevent form submission to server
    
                // Get user input
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
    
                // Call loginUser() from mock backend
                if (loginUser(email, password)) {
                    closePopup('loginPopup'); // Close login pop-up
                    updateLoginButton(); // Update the login button to "Log Out"
                }
            });
        }
    
        // Function to handle logout
        const loginButton = document.querySelector('.login-button');
        loginButton.addEventListener('click', function(event) {
            if (loginButton.textContent === 'Log Out') {
                logoutUser();
            } else {
                openSignUp(); // Open the login pop-up if user is not logged in
            }
        });
    });
    
    // Function to update login button to "Log Out"
    function updateLoginButton() {
        const loginButton = document.querySelector('.login-button');
        loginButton.textContent = 'Log Out';
        loginButton.classList.add('logout-button');
    }
    
    // Function to log out the user
    function logoutUser() {
        const loginButton = document.querySelector('.login-button');
        loginButton.textContent = 'Log In';
        loginButton.classList.remove('logout-button');
        alert('You have successfully logged out.');
    }
    