#!/usr/bin/env python3
""" Module of Session Authentication """
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Session Authentication Class

    This class provides session-based authentication functionality.
    It allows creating and managing user sessions.
    """

    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session for the given user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The session ID generated for the user.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get the user ID associated with the given session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """Get the User instance for the current request.

        Args:
            request (Request): The request to process.

        Returns:
            User: The User instance for the request.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Destroy the session for the current request.

        Args:
            request (Request): The request to process.

        Returns:
            bool: True if the session was destroyed, False otherwise.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
