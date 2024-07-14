#!/usr/bin/env python3
""" Module of Session Authentication with expiration """
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Authentication with expiration Class"""

    def __init__(self):
        """Initialize the SessionExpAuth instance"""
        self.session_duration: int = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Create a new session for the given user ID.

        Args:
            user_id : The ID of the user. Defaults to None.
        """
        session_id: str = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get the user ID associated with the given session ID.

        Args:
            session_id : The session ID to look up. Defaults to None.
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
