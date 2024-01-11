#!/usr/bin/env python3
"""
Function returns the Log Messages
"""
import re
from typing import List
import logging
import mysql.connector
import os

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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
        """Function filters values in"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


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


def get_logger() -> logging.Logger:
    """Funtion returms a user data logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Function to connect to the MySQL database using environment variables.

    Returns:
    - mysql.connector.connection.MySQLConnection: Database connector object.
    """
    username: str = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password: str = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host: str = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name: str = os.getenv("PERSONAL_DATA_DB_NAME")

    connector: MySQLConnection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connector


def main():
    """Function to retrieve all rows in the users
    table and display each row under a filtered format."""
    my_db = get_db()
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM users;")
    data = cursor.fetchall()

    log = get_logger()

    for row in data:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3],
                               row[4], row[5], row[6], row[7])
        log.info(fields)
    cursor.close()
    my_db.close()
