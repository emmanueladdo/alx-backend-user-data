#!/usr/bin/env python3
"""Basic Auth implementation module
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Auth Class"""

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """Performs base64 encoding on the auth_header
        extract base64 of auth header after "Basic "
        """
        if auth_header is None or not isinstance(auth_header, str):
            return None
        if not auth_header.startswith("Basic "):
            return None
        return auth_header.split("Basic ")[1]

    def decode_base64_authorization_header(self, b64_header: str) -> str:
        """Decodes a base64 string return base64 of string
        """
        if b64_header is None or not isinstance(b64_header, str):
            return None

        try:
            return base64.b64decode(b64_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_b64_header: str) -> (str, str):
        """extract user credentials from the Base64 decoded value
        returns the user email and password
        """
        if decoded_b64_header is None:
            return None, None
        if not isinstance(decoded_b64_header, str):
            return None, None
        if ':' not in decoded_b64_header:
            return None, None
        user_credentials = decoded_b64_header.split(':', 1)
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """return User instance based on their email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
            for usr in users:
                if usr.is_valid_password(user_pwd):
                    return usr
        except Exception:
            return None

    def current_user(self, req=None) -> TypeVar('User'):
        """retrieves the User instance for a request
        """
        auth_hdr = self.authorization_header(req)
        b64_hdr = self.extract_base64_authorization_header(auth_hdr)
        decoded = self.decode_base64_authorization_header(b64_hdr)
        credentials = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(credentials[0],
                                                 credentials[1])
        return user
