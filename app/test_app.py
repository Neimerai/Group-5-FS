import unittest
from app import app
from firebase_database import create_user, get_user_by_email, create_booking
from werkzeug.security import generate_password_hash
import random

class FlightBookingSystemTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.unique_email = self.generate_unique_email()  # Generate a unique email for each test

    # Utility method to generate a unique email
    def generate_unique_email(self):
        unique_id = random.randint(1000, 9999)
        return f"testuser{unique_id}@example.com"

    ### Requirement 6: User Registration UI

    def test_registration_form_validation(self):
        # Test missing required fields
        response = self.client.post('/signup', json={
            "first_name": "",
            "last_name": "",
            "email": self.unique_email,
            "password": "",
            "phone": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)

    def test_password_strength_validation(self):
        possible_messages = [
            "Password must be at least 8 characters long.",
            "Password must contain at least one uppercase letter.",
            "Password must contain at least one lowercase letter.",
            "Password must contain at least one number.",
            "Password must contain at least one special character.",
            "Password too weak"
        ]
        # Test weak password
        response = self.client.post('/signup', json={
            "first_name": "Weak",
            "last_name": "Password",
            "email": self.unique_email,
            "password": "weak",
            "phone": "1234567890"
        })
        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        # Check if the returned message is in the list of possible messages
        self.assertIn(json_data["message"], possible_messages)

    def test_successful_registration_submission(self):
        # Test successful registration with valid data
        response = self.client.post('/signup', json={
            "first_name": "Test",
            "last_name": "User",
            "email": self.unique_email,
            "password": "Test@1234",
            "phone": "1234567890"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"success", response.data)

    ### Requirement 7: Login UI

    def test_login_form_validation(self):
        # Test invalid email format and incorrect password
        response = self.client.post('/login', json={
            "email": "invalid-email",
            "password": "1234"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Invalid email or password", response.data)

    def test_successful_login_submission(self):
        # Ensure the user is registered first
        create_user({
            "first_name": "Test",
            "last_name": "User",
            "email": self.unique_email,
            "password": generate_password_hash("Test@1234"),
            "phone": "1234567890"
        })

        # Attempt to log in with the registered user
        response = self.client.post('/login', json={
            "email": self.unique_email,
            "password": "Test@1234"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login successful", response.data)

    ### Additional: Test Case for Booking Creation (using registered email)

    def test_create_booking(self):
        # Ensure the user exists before creating a booking
        user = get_user_by_email(self.unique_email)
        if user is None:
            user_id = create_user({
                "first_name": "Booking",
                "last_name": "Test",
                "email": self.unique_email,
                "password": generate_password_hash("Test@1234"),
                "phone": "1234567890"
            })
            user = {"user_id": user_id}

        # Create a booking
        booking_data = {
            "user_id": user.get("user_id"),
            "flight_id": "FL1234",
            "seat": "12A",
            "date": "2024-12-25"
        }
        
        booking_id = create_booking(booking_data)
        self.assertIsNotNone(booking_id, "Booking creation failed, returned None")

if __name__ == "__main__":
    unittest.main()
