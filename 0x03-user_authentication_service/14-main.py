# Filename: test_logout.py

import unittest
from flask import Flask, redirect, url_for, abort
from unittest.mock import patch, MagicMock
from app import app  # Import your Flask application

class TestLogout(unittest.TestCase):
    @patch('app.AUTH.get_user_from_session_id')
    @patch('app.AUTH.destroy_session')
    def test_logout_user_exists(self, mock_destroy_session, mock_get_user_from_session_id):
        """
        Test that logout successfully redirects if the user exists.
        """
        # Mocking
        mock_user = MagicMock()
        mock_user.id = 1
        mock_get_user_from_session_id.return_value = mock_user

        # Test client
        with app.test_client() as client:
            response = client.delete('/sessions', data={'session_id': 'valid_session_id'})
            self.assertEqual(response.status_code, 302)  # Redirect status code
            mock_destroy_session.assert_called_once_with(1)

    @patch('app.AUTH.get_user_from_session_id')
    def test_logout_user_does_not_exist(self, mock_get_user_from_session_id):
        """
        Test that logout aborts with a 403 status code if the user does not exist.
        """
        # Mocking
        mock_get_user_from_session_id.return_value = None

        # Test client
        with app.test_client() as client:
            response = client.delete('/sessions', data={'session_id': 'invalid_session_id'})
            self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()