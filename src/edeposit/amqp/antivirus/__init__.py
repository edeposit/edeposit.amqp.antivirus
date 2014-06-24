#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
"""
# Imports =====================================================================
import antivirus
import structures


# Functions & objects =========================================================
def _instanceof(instance, cls):
    """
    Check type of `instance` by matching ``.__name__`` with `cls.__name__`.
    """
    return type(instance).__name__ == cls.__name__


# Main function ===============================================================
def reactToAMQPMessage(message, UUID):
    """
    React to given (AMQP) message. `message` is usually expected to be
    :py:func:`collections.namedtuple` structure filled with all necessary data.

    Args:
        message (object): One of the request objects defined in
                          :mod:`structures`.
        UUID (str): Unique ID of received message.

    Returns:
        object: Response class from :mod:`structures`.

    Raises:
        ValueError: if bad type of `message` structure is given.
    """
    if _instanceof(message, structures.ScanFile):
        result = antivirus.save_and_scan(
            message.filename,
            message.b64_data
        )
        return structures.ScanResult(message.filename, result)

    elif _instanceof(message, structures.UpdateDatabase):
        return structures.DatabaseUpdated(
            antivirus.update_database()
        )

    raise ValueError(
        "Unknown type of request: '" + str(type(message)) + "'!"
    )
