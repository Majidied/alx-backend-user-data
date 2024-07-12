from typing import List, TypeVar
from flask import request


class Auth:
    """Class representing the authentication functionality."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method that should implement the logic for checking if a route
        requires authentication.

        Args:
            path (str): The path of the route.
            excluded_paths (List[str]): List of paths that are excluded from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True
    
    def authorization_header(self, request=None) -> str:
        """Method that should implement the logic for checking if a request
        is authorized.

        Args:
            request (Optional): The request object.

        Returns:
            str: The authorization header value if present, None otherwise.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']
    
    def current_user(self, request=None) -> TypeVar('User'):
        """Method that should implement the logic for checking if a request
        is authorized.

        Args:
            request (Optional): The request object.

        Returns:
            TypeVar('User'): The current user if authorized, None otherwise.
        """
        return None
