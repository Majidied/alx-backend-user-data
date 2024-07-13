#!/usr/bin/env python3
""" Module of Session Authentication with expiration and database storage """
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session Authentication with expiration and database storage Class"""

    def create_session(self, user_id=None):
        """
        Create a Session ID for a user_id
        Args:
           user_id (str): user id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get the user ID associated with the given session ID.

        Args:
            session_id : The session ID to look up. Defaults to None.
        """
        if session_id is None:
            return None
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id[0].user_id
        return None

    def destroy_session(self, request=None):
        """Destroy the session for the current request.

        Args:
            request : The request to process. Defaults to None.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session[0].remove()
        return True
