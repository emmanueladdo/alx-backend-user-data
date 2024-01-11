#!/usr/bin/env python3
"""
Function returns the Log Messages
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
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
    for field in fields:
        replace = "{}={}{}".format(field, redaction, separator)
        message = re.sub("{}=.*?{}".format(field, separator), replace, message)
    return message
