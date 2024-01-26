#!/usr/bin/env python3
"""
API Route Module
"""

from flask import Flask, abort, jsonify, redirect, request
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    Returns a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
    Registers new users.

    Expects 'email' and 'password' in the request form data.
    Returns a JSON payload with the user's email
    and a success message if registration is successful.
    Returns a 400 response with an error message
    if the email is already registered.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        if new_user is not None:
            return jsonify({
                "email": f"{email}",
                "message": "user created"
            }), 200
    except Exception:
        return jsonify({
            "message": "email already registered"
        }), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Creates a new session for the user.

    Expects 'email' and 'password' in the request form data.
    Sets a session ID cookie and returns a
    JSON payload with the user's email and a success message.
    Aborts with a 401 status if the login is not valid.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)

    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Finds the user with the requested session ID,
    destroys the session, and redirects the user to GET /.

    Aborts with a 403 status if there is no session
    ID cookie or if the user is not found.
    """
    cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(cookie)
    if cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Gets the user by using the session ID.

    Returns a JSON payload with the user's email.
    Aborts with a 403 status if there is no
    session ID cookie or if the user is not found.
    """
    cookie = request.cookies.get("session_id", None)
    if cookie is None:
        abort(403)
    user = AUTH.get_user_from_session_id(cookie)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Checks if the provided email is registered.

    If registered, generates a reset token and responds with
    a JSON payload containing the email and reset token.
    Aborts with a 403 status if the email is not registered.
    """
    email = request.form.get('email')
    is_registered = AUTH.create_session(email)

    if is_registered:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    else:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Updates the user's password using the provided
    reset token and new password.

    Responds with a JSON payload containing the user's
    email and a success message.
    Aborts with a 403 status if the reset token is invalid.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
