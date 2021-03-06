#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
AMQP interface used by `edeposit.amqp <http://edeposit-amqp.readthedocs.org>`_
package.
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
def reactToAMQPMessage(message, send_back):
    """
    React to given (AMQP) message. `message` is expected to be
    :py:func:`collections.namedtuple` structure from :mod:`.structures` filled
    with all necessary data.

    Args:
        message (object): One of the request objects defined in
                          :mod:`.structures`.
        send_back (fn reference): Reference to function for responding. This is
                  useful for progress monitoring for example. Function takes
                  one parameter, which may be response structure/namedtuple, or
                  string or whatever would be normally returned.

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
