#!/usr/bin/env python3
"""
Main file to test destroy_session method in Auth class
"""
from db import DB
from auth import Auth
from user import User

def test_destroy_session():
	"""
	Test the destroy_session method
	"""
	# Initialize database and Auth
	my_db = DB()
	auth = Auth()

	# Create a new user
	email = "user@example.com"
	password = "password"
	user = my_db.add_user(email, password)
	print(f"User {user.id} created")

	# Simulate creating a session for the user
	user_id = user.id
	auth._db.update_user(user_id, session_id="session_id")
	print(f"Session created for user {user_id}")

	# Destroy the session
	auth.destroy_session(user_id)
	user = my_db.find_user_by(id=user_id)
	if user.session_id is None:
		print(f"Session for user {user_id} successfully destroyed")
	else:
		print(f"Failed to destroy session for user {user_id}")

if __name__ == "__main__":
	test_destroy_session()