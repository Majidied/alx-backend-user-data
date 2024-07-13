#!/usr/bin/env python3
""" Module of Session Authentication with expiration """
from api.v1.auth.session_auth import SessionAuth
from models.user import User
from uuid import uuid4
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """Session Authentication with expiration Class"""

    def __init__(self):
        """Initialize the SessionExpAuth instance"""
        super().__init__()
        self.session_duration: int = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str = None) -> str:
        """Create a new session for the given user ID.

        Args:
            user_id (str): The ID of the user. Defaults to None.

        Returns:
            str: The session ID.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get the user ID associated with the given session ID.

        Args:
            session_id (str): The session ID to look up. Defaults to None.

        Returns:
            str: The user ID or None if session is invalid or expired.
        """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None
        if (datetime.now() - created_at) > timedelta(seconds=
                                                     self.session_duration):
            return None
        return session_dict.get("user_id")
