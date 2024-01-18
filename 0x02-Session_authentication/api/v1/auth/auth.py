#!/usr/bin/env python3
"""
manages the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    Class that defines the authenication of API
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """authorithation requirement check"""
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if p.endswith('*'):
                if path.startswith(p[:1]):
                    return False
        return False if path in excluded_paths else True

    def authorization_header(self, request=None) -> str:
        """header check"""
        if request:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user"""
        return None


    def session_cookie(self, request=None):
        """
        function returns cookie value from a request
        """
        if request is None:
            return None
        _my_session_id = getenv("SESSION_NAME")
        return request.cookies.get(_my_session_id)