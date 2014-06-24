#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Wrapper over ``freshclam`` program to update database over amqp.
"""
# Imports =====================================================================
import os
from functools import wraps


import sh


# Functions & objects =========================================================
def require_root(fn):
    """
    Decorator to make sure, that user is root.
    """
    @wraps(fn)
    def xex(*args, **kwargs):
        assert os.geteuid() == 0, \
            "You have to be root to run function '%s'." % fn.__name__
        return fn(*args, **kwargs)

    return xex


@require_root
def update_database():
    """
    Run ``freshclam``. Make sure, that user is root.
    """
    return sh.freshclam()
