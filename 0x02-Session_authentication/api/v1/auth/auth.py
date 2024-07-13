#!/usr/bin/env python3
"""Authentication module.
"""
from flask import request
from typing import List, TypeVar
import fnmatch
import os


class Auth:
    """Authentication class."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to check if auth is required."""
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip("/")

        for ep in excluded_paths:
            if fnmatch.fnmatch(path, ep.rstrip("/")):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Method to get authorization header."""
        if request is not None:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Method to get user from request."""
        return None

    def session_cookie(self, request=None) -> str:
        """Method to get session cookie."""
        if request is not None:
            session_name = os.getenv('SESSION_NAME', '_my_session_id')
            return request.cookies.get(session_name)
        return None
