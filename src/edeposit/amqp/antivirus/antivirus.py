#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import wrappers.clamd as clamd
import wrappers.clamscan as clamscan
import settings


# Functions & objects =========================================================
def scan_file(path):
    """
    Scan `path` for viruses using ``clamd`` or ``clamscan`` (depends on
    :attr:`settings.USE_CLAMD`.

    Args:
        path (str): Relative or absolute path of file/directory you need to
                    scan.

    Returns:
        dict: ``{filename: ("FOUND", "virus type")}`` or blank dict.

    Raises:
        ValueError: When the server is not running.
        AssertionError: When the internal file doesn't exists.
    """
    if settings.USE_CLAMD:
        return clamd.scan_file(path)
    else:
        return clamscan.scan_file(path)
