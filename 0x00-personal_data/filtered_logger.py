#!/usr/bin/env python3
"""
Function returns the Log Messages
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specified fields in the log message using regex.

    Args:
    - fields: List of strings representing fields to obfuscate.
    - redaction: String representing the obfuscation value.
    - message: String representing the log line.
    - separator: String representing the character
    separating fields in the log line.
    Returns:
    - String: Obfuscated log message.
    """
    for item in fields:
        replace = "{}={}{}".format(item, redaction, separator)
        message = re.sub("{}=.*?{}".format(item, separator), replace, message)
    return message
