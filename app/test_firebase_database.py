import unittest
from unittest.mock import patch, MagicMock
from firebase_database import create_user, get_user_by_email, create_booking, get_bookings_by_user, update_booking, delete_booking

class TestFirebaseDatabase(unittest.TestCase):

    @patch('firebase_database.users_ref')
    def test_create_user_success(self, mock_users_ref):
        # Mock user reference push and set
        mock_push = MagicMock()
        mock_push.key = 'unique_user_key'
        mock_users_ref.push.return_value = mock_push

        user_data = {"email": "test@example.com", "password": "hashed_password"}
        result = create_user(user_data)
        self.assertEqual(result, 'unique_user_key')

    @patch('firebase_database.users_ref')
    def test_create_user_exception(self, mock_users_ref):
        # Simulate an exception in users_ref.push().set()
        mock_users_ref.push.side_effect = Exception("Database error")
        result = create_user({"email": "test@example.com"})
        self.assertIsNone(result)

    @patch('firebase_database.users_ref')
    def test_get_user_by_email_found(self, mock_users_ref):
        # Simulate a snapshot with user data
        mock_snapshot = {'user123': {"email": "test@example.com"}}
        mock_users_ref.order_by_child.return_value.equal_to.return_value.get.return_value = mock_snapshot

        result = get_user_by_email("test@example.com")
        self.assertEqual(result, {"email": "test@example.com", "user_id": "user123"})

    @patch('firebase_database.users_ref')
    def test_get_user_by_email_not_found(self, mock_users_ref):
        # Simulate an empty snapshot
        mock_users_ref.order_by_child.return_value.equal_to.return_value.get.return_value = {}
        result = get_user_by_email("nonexistent@example.com")
        self.assertIsNone(result)

    @patch('firebase_database.bookings_ref')
    def test_create_booking_success(self, mock_bookings_ref):
        # Mock booking reference push and set
        mock_push = MagicMock()
        mock_push.key = 'unique_booking_key'
        mock_bookings_ref.push.return_value = mock_push

        booking_data = {"from": "CityA", "to": "CityB"}
        result = create_booking(booking_data)
        self.assertEqual(result, 'unique_booking_key')

    @patch('firebase_database.bookings_ref')
    def test_create_booking_exception(self, mock_bookings_ref):
        # Simulate an exception in bookings_ref.push().set()
        mock_bookings_ref.push.side_effect = Exception("Database error")
        result = create_booking({"from": "CityA", "to": "CityB"})
        self.assertIsNone(result)

    @patch('firebase_database.bookings_ref')
    def test_get_bookings_by_user_found(self, mock_bookings_ref):
        # Mock bookings snapshot with booking data
        mock_snapshot = {'booking123': {"userId": "user123"}}
        mock_bookings_ref.order_by_child.return_value.equal_to.return_value.get.return_value = mock_snapshot

        result = get_bookings_by_user("user123")
        self.assertEqual(result, mock_snapshot)

    @patch('firebase_database.bookings_ref')
    def test_get_bookings_by_user_not_found(self, mock_bookings_ref):
        # Simulate an empty snapshot
        mock_bookings_ref.order_by_child.return_value.equal_to.return_value.get.return_value = {}
        result = get_bookings_by_user("nonexistent_user")
        self.assertEqual(result, {})

    @patch('firebase_database.bookings_ref')
    def test_update_booking_success(self, mock_bookings_ref):
        # Mock update
        booking_id = 'booking123'
        new_data = {"from": "CityA", "to": "CityB"}
        mock_booking_ref = MagicMock()
        mock_bookings_ref.child.return_value = mock_booking_ref
        update_booking(booking_id, new_data)
        mock_booking_ref.update.assert_called_once_with(new_data)

    @patch('firebase_database.bookings_ref')
    def test_update_booking_exception(self, mock_bookings_ref):
        # Simulate an exception in bookings_ref.child().update()
        mock_booking_ref = MagicMock()
        mock_booking_ref.update.side_effect = Exception("Database error")
        mock_bookings_ref.child.return_value = mock_booking_ref
        update_booking("booking123", {"from": "CityA"})  # Should not raise an error despite the exception

    @patch('firebase_database.bookings_ref')
    def test_delete_booking_success(self, mock_bookings_ref):
        # Mock delete
        booking_id = 'booking123'
        mock_booking_ref = MagicMock()
        mock_bookings_ref.child.return_value = mock_booking_ref
        delete_booking(booking_id)
        mock_booking_ref.delete.assert_called_once()

    @patch('firebase_database.bookings_ref')
    def test_delete_booking_exception(self, mock_bookings_ref):
        # Simulate an exception in bookings_ref.child().delete()
        mock_booking_ref = MagicMock()
        mock_booking_ref.delete.side_effect = Exception("Database error")
        mock_bookings_ref.child.return_value = mock_booking_ref
        delete_booking("booking123")  # Should not raise an error despite the exception

if __name__ == "__main__":
    unittest.main()
