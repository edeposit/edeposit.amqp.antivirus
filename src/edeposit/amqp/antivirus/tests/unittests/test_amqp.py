#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import antivirus
from antivirus import structures 
import antivirus.antivirus as av_wrapper


# Functions & objects =========================================================
def test_clamd_detection():
    av_wrapper.save_and_scan = lambda x, y: 1
    reload(antivirus)

    fn = "/path/to/file"
    result = antivirus.reactToAMQPMessage(
        structures.ScanFile(fn, "data"),
        "11"
    )

    assert isinstance(result, structures.ScanResult), "Bad structure returned!"
    assert result.filename == fn
    assert result.result == 1


def test_clamd_update():
    av_wrapper.update_database = lambda: 1
    reload(antivirus)

    result = antivirus.reactToAMQPMessage(
        structures.UpdateDatabase(),
        "11"
    )

    assert isinstance(result, structures.DatabaseUpdated), "Bad structure returned!"
    assert result.log == 1
