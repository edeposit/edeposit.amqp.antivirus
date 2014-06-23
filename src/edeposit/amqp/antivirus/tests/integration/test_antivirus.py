#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import time


from antivirus import settings
from antivirus import antivirus


# Variables ===================================================================
EICAR_B64 = """
WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNU
LUZJTEUhJEgrSCo=
"""

CLEAN = """
IyEgL3Vzci9iaW4vZW52IGJhc2gKRklMRUxJU1Q9YHppcGluZm8gLTEgIiR7MX0iIHwgZ3JlcCAi
XC5odG1sIiB8c29ydGAKVEVYVD0iIgpmb3IgRklMRSBpbiAkRklMRUxJU1QKZG8KICAgIFRFWFQ9
IiR7VEVYVH0gYHVuemlwIC1jYWEgIiR7MX0iICIke0ZJTEV9IiB8IGh0bWwydGV4dCAtd2lkdGgg
NzBgIgpkb25lCmVjaG8gIiR7VEVYVH0iIHxsZXNzCg==
"""



# Functions & objects =========================================================
def test_clamd_detection():
    result = antivirus.save_and_scan("/home/bystrousak/eicar.com", EICAR_B64)

    fn = result.keys()[0]
    assert result
    assert result[fn][0] == "FOUND"
    assert result[fn][1] == "Eicar-Test-Signature"


def test_clamd_clean():
    result = antivirus.save_and_scan("/home/bystrousak/conv.sh", CLEAN)

    assert not result


def test_clamscan_detection():
    settings.USE_CLAMD = False
    reload(antivirus)

    t_start = time.time()
    result = antivirus.save_and_scan("/home/bystrousak/eicar.com", EICAR_B64)
    t_end = time.time()

    assert t_end - t_start > 2

    fn = result.keys()[0]
    assert result
    assert result[fn][0] == "FOUND"
    assert result[fn][1] == "Eicar-Test-Signature"


def test_clamscan_clean():
    settings.USE_CLAMD = False
    reload(antivirus)

    result = antivirus.save_and_scan("/home/bystrousak/conv.sh", CLEAN)
    assert not result
