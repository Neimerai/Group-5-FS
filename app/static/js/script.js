// Function to show a popup by ID
function showPopup(id) {
    const popup = document.getElementById(id);
    if (popup) {
        popup.classList.remove('hidden');
    }
}

// Function to hide a popup by ID
function closePopup(id) {
    const popup = document.getElementById(id);
    if (popup) {
        popup.classList.add('hidden');
    }
}

// Toggle between showing Login and Register popups
function showLogin() {
    closePopup('registerPopup');
    showPopup('loginPopup');
}

function showSignUp() {
    closePopup('loginPopup');
    showPopup('registerPopup');
}

// Update Login Button to show "Log Out" if the user is logged in
function updateLoginButton() {
    const loginButton = document.querySelector('.login-button');
    if (loginButton) {
        loginButton.textContent = "Log Out";
        loginButton.onclick = logout;
    }
}

// Logout function
function logout() {
    fetch('/logout')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload(); // Reload the page after logout
            }
        })
        .catch(error => console.error('Error during logout:', error));
}

// Register Form Submission
const registerForm = document.querySelector('#registerPopup form');
if (registerForm) {
    registerForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission to server

        // Get user input
        const newUser = {
            first_name: document.getElementById('first-name').value,
            last_name: document.getElementById('last-name').value,
            email: document.getElementById('sign-up-email').value,
            phone: document.getElementById('phone').value,
            password: document.getElementById('sign-up-password').value
        };

        // Send POST request to Flask backend
        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newUser)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Registration successful!');
                showLogin(); // Show login popup after successful signup
            } else {
                alert(data.message || 'Signup failed');
            }
        })
        .catch(error => {
            console.error('Error during signup:', error);
            alert('An error occurred during signup.');
        });
    });
}

// Login Form Submission
const loginForm = document.querySelector('#loginPopup form');
if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission to server

        // Get user input
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Send POST request to Flask backend
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Login successful');
                closePopup('loginPopup'); // Close login popup
                updateLoginButton(); // Update login button to "Log Out"
            } else {
                alert(data.message || 'Login failed');
            }
        })
        .catch(error => {
            console.error('Error during login:', error);
            alert('An error occurred during login.');
        });
    });
}

// Function to submit the booking form
function submitForm() {
    const from = document.getElementById('from').value;
    const to = document.getElementById('to').value;
    const departure = document.getElementById('departure').value;
    const returnDate = document.getElementById('return').value;
    const directFlight = document.getElementById('direct-flight').checked;
    const hotelIncluded = document.getElementById('hotel-included').checked;

    fetch('/bookings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            from,
            to,
            departure,
            return_date: returnDate,
            direct_flight: directFlight,
            hotel_included: hotelIncluded
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Booking created successfully!');
        } else {
            alert(data.message || 'Booking failed');
        }
    })
    .catch(error => {
        console.error('Error during booking creation:', error);
        alert('An error occurred while creating the booking.');
    });
}

// Filtering airports (simulated example; ideally, this would pull data from an API or database)
function filterAirports(inputId) {
    const input = document.getElementById(inputId);
    const dropdown = document.getElementById(`${inputId}-dropdown`);

    // Example filtering logic
    const airports = ["JFK", "LAX", "ORD", "ATL", "DFW", "DEN", "SFO"];
    dropdown.innerHTML = '';
    airports.forEach(airport => {
        if (airport.toLowerCase().includes(input.value.toLowerCase())) {
            const option = document.createElement('div');
            option.textContent = airport;
            option.onclick = () => {
                input.value = airport;
                dropdown.innerHTML = '';
            };
            dropdown.appendChild(option);
        }
    });

    // Show dropdown if input has text; hide otherwise
    dropdown.style.display = input.value ? 'block' : 'none';
}
