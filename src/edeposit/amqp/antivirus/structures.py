#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Definitions of the communication structures used in edeposit.amqp.antivirus
project.
"""
# Imports =====================================================================
from collections import namedtuple


# Requests ====================================================================
class ScanFile(namedtuple("ScanFile", ["filename", "b64_data"])):
    """
    Request to scan file.

    Args:
        filename (str): Path of the file at your system. It will be used in
                 result structure.
        b64_data (str): Base64 encoded content of the file.

    Returns:
        object: :class:`ScanResult`
    """
    pass


class UpdateDatabase(namedtuple("UpdateDatabase", [])):
    """
    Request to update clamav database (= to run ``freshclam`` program).

    Returns:
        object: :class:`DatabaseUpdated`
    """
    pass


# Responses ===================================================================
class ScanResult(namedtuple("ScanResult", ["filename", "result"])):
    """
    Result of the file scan.

    Args:
        filename (str): Name of the file as was specified in :class:`ScanFile`
                 request.
        result (dict): Dictionary in following format:

    ::

        {
            "local_path": ("RESULT", "TYPE")
        }

    Where `RESULT` is "FOUND" or string like that and `TYPE` is name of the
    malware.

    Note:
        When no malware is found, :attr:`result` is blank dict.
    """
    pass


class DatabaseUpdated(namedtuple("DatabaseUpdated", ["log"])):
    """
    Response to :class:`UpdateDatabase`.

    Attr:
        log (str): Log of the ``freshclam`` run.
    """
    pass
