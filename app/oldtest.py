import unittest
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_form_display(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)

    def test_login_post(self):
        response = self.app.post('/', data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome Back!', response.data)

    def test_sign_up_form_display(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create a new account', response.data)

    def test_sign_up_post(self):
        response = self.app.post('/', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone': '1234567890',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book your flights today', response.data)

    def test_flight_search_form_display(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter departure airport', response.data)

    def test_flight_search_post(self):

        response = self.app.post('/search-flights', json={
            'from': 'Toronto Pearson International (YYZ)',
            'to': 'London Heathrow (LHR)',
            'departure': '2024-11-01',
            'return': '2024-11-15',
            'directFlight': True,
            'hotelIncluded': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flights found:', response.data)

if __name__ == '__main__':
    unittest.main()
