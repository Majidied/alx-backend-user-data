#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import re
import base64
import binascii
from typing import Tuple, Optional, TypeVar

from .auth import Auth
from models.user import User

UserType = TypeVar('UserType', bound='User')


class BasicAuth(Auth):
    """Basic authentication class.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: Optional[str]) -> Optional[str]:
        """Extracts the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if isinstance(authorization_header, str):
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: Optional[str]) -> Optional[str]:
        """Decodes a base64-encoded authorization header.
        """
        if isinstance(base64_authorization_header, str):
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None
        return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: Optional[str],
            ) -> Tuple[Optional[str], Optional[str]]:
        """Extracts user credentials from a base64-decoded authorization
        header that uses the Basic authentication flow.
        """
        if isinstance(decoded_base64_authorization_header, str):
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: Optional[str],
            user_pwd: Optional[str]) -> Optional[UserType]:
        """Retrieves a user based on the user's authentication credentials.
        """
        if isinstance(user_email, str) and isinstance(user_pwd, str):
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) == 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> Optional[UserType]:
        """Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        if b64_auth_token is None:
            return None
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        if auth_token is None:
            return None
        email, password = self.extract_user_credentials(auth_token)
        if email is None or password is None:
            return None
        return self.user_object_from_credentials(email, password)
