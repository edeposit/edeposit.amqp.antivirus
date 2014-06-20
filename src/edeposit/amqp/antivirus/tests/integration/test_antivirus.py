#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import antivirus


# Variables ===================================================================
EICAR_B64 = """
WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNULUZ
JTEUhJEgrSCo="""


# Functions & objects =========================================================
def test_clamd_detection():
    antivirus.save_and_scan("/home/bystrousak/eicar.com", EICAR_B64)

def test_clamd_clean():
    pass

def test_clamscan_detection():
    pass  # TODO: Don't forget to test time.

def test_clamscan_clean():
    pass
