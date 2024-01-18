#!/usr/bin/env python3
"""
Session Authentication Module

This module defines a SessionAuth class that provides session-based
authentication methods. It includes functionality to create and manage
user sessions, retrieve User IDs based on session IDs, retrieve the
current user based on a cookie value, and destroy user sessions (logout).
"""

from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Session Auth Class

    This class extends the Auth class and provides additional methods
    for session-based authentication. It includes functionality to create
    and manage user sessions, retrieve User IDs based on session IDs,
    retrieve the current user based on a cookie value, and destroy user
    sessions (logout).
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create Session ID for User

        Args:
            user_id (str): User ID

        Returns:
            str: Session ID for the created session
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Get User ID for Session ID

        Args:
            session_id (str): Session ID

        Returns:
            str: User ID associated with the given session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Get Current User based on Cookie Value

        Args:
            request: Flask request object

        Returns:
            User: User instance corresponding to the current session
        """
        _my_session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(_my_session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Destroy User Session (Logout)

        Args:
            request: Flask request object

        Returns:
            bool: True if the session
            is successfully destroyed, False otherwise
        """
        if request is None:
            return None
        _my_session_id = self.session_cookie(request)
        if not _my_session_id:
            return False
        user_id = self.user_id_for_session_id(_my_session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[_my_session_id]
        return True
