#!/usr/bin/env python3
"""
Function returns the Log Messages
"""
import re
from typing import List
import logging

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)


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
    for element in fields:
        replace = "{}={}{}".format(element, redaction, separator)
        message = re.sub("{}=.*?{}".format(element, separator),
                         replace, message)
    return message
