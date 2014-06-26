#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module is containing all necessary global variables for the package.

Module also has the ability to read user-defined data from two paths:

- ``$HOME/_SETTINGS_PATH``
- ``/etc/_SETTINGS_PATH``

See :attr:`._SETTINGS_PATH` for details.

Note:
    If the first path is found, other is ignored.

Example of the configuration file (``$HOME/edeposit/antivirus.json``)::

    {
        "USE_CLAMD": false
    }

Attributes
----------
"""
import json
import os
import os.path


# Functions ===================================================================
def is_deb_system():
    """
    Badly written test whether the system is deb/apt based or not.
    """
    return os.path.exists("/etc/apt")


# Module configuration ========================================================
#: True - ``clamd`` daemon will be used, False - ``clamscan`` will be used.
#: ``clamscan`` takes much less memory, but takes a LOT more time to scan.
#: ``clamd`` takes huge amouts of memory (500MB min), but scans in fractions of
#: seconds.
USE_CLAMD = True

#: Configuration file directory at debian systems.
DEB_CONF_PATH = "/etc/clamav/"

#: Configuration file directory at suse systems.
SUSE_CONF_PATH = "/etc/"

#: Name of the configuration file.
CONF_FILE = "clamd.conf"

#: Path to the configuration file.
CONF_PATH = (DEB_CONF_PATH if is_deb_system() else SUSE_CONF_PATH) + CONF_FILE

#: Path to the local unix socket - don't change this if you are not sure (it
#: will break things).
LOCALSOCKET = "/var/run/clamav/clamd.ctl"

#: Path to the pid file - don't change this if you are not sure (it will break
#: things).
PIDFILE = "/var/run/clamav/clamd.pid"

#: Path to the log file.
LOGFILE = "/var/log/clamav/clamav.log"


# User configuration reader (don't edit this ==================================
_ALLOWED = [str, int, float]

_SETTINGS_PATH = "/edeposit/ftp.json"
"""
Path which is appended to default search paths (``$HOME`` and ``/etc``).

Note:
    It has to start with ``/``. Variable is **appended** to the default search
    paths, so this doesn't mean, that the path is absolute!
"""


def get_all_constants():
    """
    Get list of all uppercase, non-private globals (doesn't start with ``_``).

    Returns:
        list: Uppercase names defined in `globals()` (variables from this \
              module).
    """
    return filter(
        lambda key: key.upper() == key and type(globals()[key]) in _ALLOWED,

        filter(                               # filter _PRIVATE variables
            lambda x: not x.startswith("_"),
            globals()
        )
    )


def substitute_globals(config_dict):
    """
    Set global variables to values defined in `config_dict`.

    Args:
        config_dict (dict): dictionary with data, which are used to set \
                            `globals`.

    Note:
        `config_dict` have to be dictionary, or it is ignored. Also all
        variables, that are not already in globals, or are not types defined in
        :attr:`_ALLOWED` (str, int, float) or starts with ``_`` are silently
        ignored.
    """
    constants = get_all_constants()

    if type(config_dict) != dict:
        return

    for key in config_dict:
        if key in constants and type(config_dict[key]) in _ALLOWED:
            globals()[key] = config_dict[key]


# try to read data from configuration paths ($HOME/_SETTINGS_PATH,
# /etc/_SETTINGS_PATH)
if "HOME" in os.environ and os.path.exists(os.environ["HOME"] + _SETTINGS_PATH):
    with open(os.environ["HOME"] + _SETTINGS_PATH) as f:
        substitute_globals(json.loads(f.read()))
elif os.path.exists("/etc" + _SETTINGS_PATH):
    with open("/etc" + _SETTINGS_PATH) as f:
        substitute_globals(json.loads(f.read()))
