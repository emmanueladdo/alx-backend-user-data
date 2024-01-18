#!/usr/bin/env python3
"""
manages the API authentication
"""
from flask import request
from typing import List, Pattern, TypeVar


class auth():
    """
    Class that defines the authenication of API
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """authentication required"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if path in excluded_paths or path + "/" in excluded_paths:
            return False

        for e_path in excluded_paths:
            if e_path.endswith('*'):
                if path.startswith(i[:1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """function add authorization header"""
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """this method gets the current user"""
        None
