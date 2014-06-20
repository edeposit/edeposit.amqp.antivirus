#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
API for scanning files using ``clamscan`` standalone program.
"""
# Imports =====================================================================
import os.path


import sh


# Functions & objects =========================================================
def _parse_result(result):
    """
    Parse ``clamscan`` output into same dictionary structured used by
    ``pyclamd``.

    Input example::
        /home/bystrousak/Plocha/prace/test/eicar.com: Eicar-Test-Signature FOUND

    Output dict::
        {
            "/home/bystrousak/Plocha/prace/test/eicar.com": (
                "FOUND",
                "Eicar-Test-Signature"
            )
        }
    """
    lines = filter(lambda x: x.strip(), result.splitlines())  # rm blank lines

    if not lines:
        return {}

    out = {}
    for line in lines:
        line = line.split(":")
        fn = line[0].strip()

        line = " ".join(line[1:])

        line = line.rsplit(None, 1)
        status = line.pop().strip()

        out[fn] = (status, " ".join(line).strip())

    return out


def scan_file(path):
    """
    Scan `path` for viruses using ``clamscan`` program.

    Args:
        path (str): Relative or absolute path of file/directory you need to
                    scan.

    Returns:
        dict: ``{filename: ("FOUND", "virus type")}`` or blank dict.

    Raises:
        AssertionError: When the internal file doesn't exists.
    """
    path = os.path.abspath(path)
    assert os.path.exists(path), "Unreachable file '%s'." % path

    result = sh.clamscan(path, no_summary=True, infected=True, _ok_code=[0, 1])

    return _parse_result(result)
