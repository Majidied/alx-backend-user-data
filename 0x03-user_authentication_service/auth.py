#!/usr/bin/env python3
""" Auth class to interact with the authentication database. """
from bcrypt import hashpw, gensalt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hash a password"""
    return hashpw(password.encode("utf-8"), gensalt())


from db import DB


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """ Initialize a new Auth instance. """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly registered user.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))
    
    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user's login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the user's credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return user.hashed_password == hashpw(password.encode("utf-8"), user.hashed_password)
        except NoResultFound:
            return False
