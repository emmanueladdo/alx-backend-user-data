#!/usr/bin/env python3
"""
This module contains functions for securely
handling user passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a provided password and returns the
    hashed password as a byte string.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted, hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain-text password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
