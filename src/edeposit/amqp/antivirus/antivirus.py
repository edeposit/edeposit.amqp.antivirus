#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
ClamAV wrapper to scan files for malware.
"""
# Imports =====================================================================
import os

import os.path
from base64 import b64decode
from tempfile import NamedTemporaryFile as NTFile


import wrappers.clamd as clamd
import wrappers.clamscan as clamscan
from wrappers.freshclam import update_database
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
    path = os.path.abspath(path)
    if settings.USE_CLAMD:
        return clamd.scan_file(path)
    else:
        return clamscan.scan_file(path)


def save_and_scan(filename, b64_data):
    """
    Save `b64_data` to temporary file and scan it for viruses.

    Args:
        filename (str): Name of the file - used as basename for tmp file.
        b64_data (str): Content of the file encoded in base64.

    Returns:
        dict: ``{filename: ("FOUND", "virus type")}`` or blank dict.
    """
    with NTFile(suffix="_"+os.path.basename(filename), mode="wb") as ifile:
        ifile.write(
            b64decode(b64_data)
        )
        ifile.flush()

        os.chmod(ifile.name, 0755)

        return scan_file(ifile.name)
