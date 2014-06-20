#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
API for scanning files using ``clamd`` daemon.
"""
# Imports =====================================================================
import os.path

import pyclamd


# Functions & objects =========================================================
def scan_file(path):
    """
    Scan `path` for viruses using ``clamd`` antivirus daemon.

    Args:
        path (str): Relative or absolute path of file/directory you need to
                    scan.

    Returns:
        dict: ``{filename: ("FOUND", "virus type")}`` or blank dict.

    Raises:
        ValueError: When the server is not running.
        AssertionError: When the internal file doesn't exists.
    """
    path = os.path.abspath(path)
    assert os.path.exists(path), "Unreachable file '%s'." % path

    try:
        cd = pyclamd.ClamdUnixSocket()
        cd.ping()
    except pyclamd.ConnectionError:
        cd = pyclamd.ClamdNetworkSocket()
        try:
            cd.ping()
        except pyclamd.ConnectionError:
            raise ValueError(
                "Couldn't connect to clamd server using unix/network socket."
            )

    cd = pyclamd.ClamdUnixSocket()
    assert cd.ping(), "clamd server is not reachable!"

    result = cd.scan_file(path)

    return result if result else {}  # result is dict or None, we need dict
