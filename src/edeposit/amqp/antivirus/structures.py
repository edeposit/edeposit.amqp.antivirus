#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Requests ====================================================================
class ScanFile(namedtuple("ScanFile", ["filename", "b64_data"])):
    pass


class UpdateDatabase(namedtuple("UpdateDatabase", [])):
    pass


# Responses ===================================================================
class ScanResult(namedtuple("ScanResult", ["filename", "result"])):
    pass


class DatabaseUpdated(namedtuple("DatabaseUpdated", ["log"])):
    pass
