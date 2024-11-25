import unittest
import uuid
from app import app


class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the Flask test client and initialize unique data for tests."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testsecret'
        cls.client = app.test_client()
        cls.random_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
        cls.password = "Test@1234"

    def test_full_flow(self):
        """Test the complete flow: signup, login, create booking, get bookings, and logout."""
        with self.client as client:
            # Step 1: Signup
            signup_data = {
                "email": self.random_email,
                "password": self.password,
                "first_name": "Integration",
                "last_name": "Test",
                "phone": "1234567890"
            }
            response = client.post('/signup', json=signup_data)
            self.assertEqual(response.status_code, 200, f"Signup failed: {response.json}")
            self.assertIn("Signup successful", response.json["message"])

            # Step 2: Login
            login_data = {
                "email": self.random_email,
                "password": self.password
            }
            response = client.post('/login', json=login_data)
            self.assertEqual(response.status_code, 200, f"Login failed: {response.json}")
            self.assertIn("Login successful", response.json["message"])

            # Step 3: Create a booking
            booking_data = {
                "from": "New York",
                "to": "Toronto",
                "departure": "2024-12-01",
                "return_date": "2024-12-10",
                "direct_flight": True,
                "hotel_included": True
            }
            response = client.post('/bookings', json=booking_data)
            self.assertEqual(
                response.status_code, 
                200, 
                f"Booking creation failed: {response.json}"
            )
            self.assertIn("Booking created", response.json["message"])

            # Step 4: Get bookings
            response = client.get('/my_bookings')
            self.assertEqual(
                response.status_code, 
                200, 
                f"Get bookings failed: {response.json}"
            )
            self.assertIn("bookings", response.json)
            self.assertIsInstance(response.json["bookings"], dict)

            # Step 5: Logout
            response = client.get('/logout')
            self.assertEqual(
                response.status_code, 
                200, 
                f"Logout failed: {response.json}"
            )
            self.assertIn("Logged out", response.json["message"])

            # Step 6: Verify access to protected routes after logout fails
            response = client.get('/my_bookings')
            self.assertEqual(response.status_code, 401, f"Access to protected route succeeded unexpectedly: {response.json}")
            self.assertIn("User not logged in", response.json["message"])


if __name__ == '__main__':
    unittest.main()