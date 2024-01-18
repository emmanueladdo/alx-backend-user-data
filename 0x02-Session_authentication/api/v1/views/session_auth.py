#!/usr/bin/env python3
"""
Session Views Module

This module defines views for session-related authentication endpoints.
"""

from os import getenv
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login() -> str:
    """Session Login View

    Route: /auth_session/login
    Method: POST

    Returns:
        str: JSON response containing user data or error message
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        _my_session_id = auth.create_session(users[0].id)
        user_data = jsonify(users[0].to_json())
        session_name = getenv("SESSION_NAME")
        user_data.set_cookie(session_name, _my_session_id)
        return user_data, 200


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """Session Logout View

    Route: /auth_session/logout
    Method: DELETE

    Returns:
        str: JSON response indicating success or error
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
