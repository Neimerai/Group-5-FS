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

const airports = [
    "Toronto Pearson International (YYZ)",
    "London Heathrow (LHR)",
    "Los Angeles International (LAX)",
    "John F. Kennedy International (JFK)",
    "Chicago O'Hare International (ORD)",
    "Dubai International (DXB)",
    "Tokyo Haneda Airport (HND)",
    "Sydney Kingsford Smith Airport (SYD)",
    "Paris Charles de Gaulle Airport (CDG)",
    "Frankfurt Airport (FRA)"
];

function filterAirports(field) {
    const input = document.getElementById(field);
    const dropdown = document.getElementById(`${field}-dropdown`);
    dropdown.innerHTML = ''; 
    const query = input.value.toLowerCase();

    if (query) {

        const filteredAirports = airports.filter(airport => airport.toLowerCase().includes(query));

        filteredAirports.forEach(airport => {
            const option = document.createElement('div');
            option.textContent = airport;
            option.onclick = () => selectAirport(field, airport);
            dropdown.appendChild(option);
        });

        dropdown.style.display = 'block';
        dropdown.style.top = `${input.offsetHeight + 20}px`;
        dropdown.style.left = '0';
        dropdown.style.width = `${input.offsetWidth}px`;
    } else {
        dropdown.style.display = 'none';
    }
}

function selectAirport(field, airport) {
    document.getElementById(field).value = airport;
    document.getElementById(`${field}-dropdown`).style.display = 'none';
}

function submitForm() {
    const from = document.getElementById('from').value;
    const to = document.getElementById('to').value;
    const departure = document.getElementById('departure').value;
    const returnDate = document.getElementById('return').value;
    const directFlight = document.getElementById('direct-flight').checked;
    const hotelIncluded = document.getElementById('hotel-included').checked;

    if (!from || !to || !departure || !returnDate) {
        alert('Please fill in all fields before searching.');
        return;
    }

    const requestData = {
        from,
        to,
        departure,
        returnDate,
        directFlight,
        hotelIncluded
    };

    // Send a POST request to the server
    fetch('http://localhost:5000/search-flights', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let flightInfo = 'Flights found:\n';
            data.flights.forEach(flight => {
                flightInfo += `Airline: ${flight.airline}, Price: $${flight.price}, Direct: ${flight.direct ? 'Yes' : 'No'}, Hotel Included: ${flight.hotelIncluded ? 'Yes' : 'No'}\n`;
            });
            alert(flightInfo);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while searching for flights.');
    });
}
