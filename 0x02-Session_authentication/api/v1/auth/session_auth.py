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

    user_id_by_session_id = {}
    
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
