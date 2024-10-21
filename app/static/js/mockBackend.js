// Mock backend data: User data (simulating a database)
let users = [
    {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
        phone: '1234567890',
        password: 'password123'
    }
];

// Function to register a new user
function registerUser(newUser) {
    // Check if user already exists by email
    const userExists = users.some(user => user.email === newUser.email);

    if (userExists) {
        alert('User with this email already exists.');
        return false;
    } else {
        // Add new user to the mock "database"
        users.push(newUser);
        alert('Registration successful!');
        return true;
    }
}

// Function to log in an existing user
function loginUser(email, password) {
    // Check if user exists and if the password matches
    const user = users.find(user => user.email === email && user.password === password);

    if (user) {
        alert(`Welcome back, ${user.firstName}!`);
        return true;
    } else {
        alert('Invalid email or password.');
        return false;
    }
}


