#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import sys
import shutil
import os.path
import logging
import argparse


try:
    import edeposit.amqp.antivirus as antivirus
    from edeposit.amqp.antivirus import settings
except ImportError:
    sys.path.insert(0, os.path.abspath('../src/edeposit/amqp'))
    import antivirus
    from antivirus import settings


# Variables ===================================================================
logging.basicConfig()
logger = logging.getLogger(__name__)


REQUIRED_SETTINGS = {
    "User": "$username",
    "LocalSocketGroup": "$groupname",
    "LocalSocket": "/var/run/clamav/clamd.ctl",
    "LogFile": "/var/log/clamav/clamav.log",
    "PidFile": "/var/run/clamav/clamd.pid",
    "MaxThreads": "2",
    "MaxConnectionQueueLength": "3",
    "LogSyslog": "false",
    "LogRotate": "true",
    "ScanELF": "true",
    "ScanPE": "true",
    "ScanArchive": "true",
    "AllowSupplementaryGroups": "true",
    "LocalSocketMode": "666",
    "FixStaleSocket": "true",
    "LogTime": "true",
    "ReadTimeout": "180",
}


# Functions & objects =========================================================
def add_or_update(data, item, value):
    """
    Add or update value in configuration file format used by proftpd.

    Args:
        data (str): Configuration file as string.
        item (str): What option will be added/updated.
        value (str): Value of option.

    Returns:
        str: updated configuration
    """
    data = data.splitlines()

    # to list of bytearrays (this is useful, because their reference passed to
    # other functions can be changed, and it will change objects in arrays
    # unlike strings)
    data = map(lambda x: bytearray(x), data)

    # search for the item in raw (ucommented) values
    conf = filter(lambda x: x.strip() and x.strip().split()[0] == item, data)

    if conf:
        conf[0][:] = conf[0].strip().split()[0] + " " + value
    else:
        # search for the item in commented values, if found, uncomment it
        comments = filter(
            lambda x: x.strip().startswith("#")
                      and len(x.split("#")) >= 2
                      and x.split("#")[1].split()
                      and x.split("#")[1].split()[0] == item,
            data
        )

        if comments:
            comments[0][:] = comments[0].split("#")[1].split()[0] + " " + value
        else:
            # add item, if not found in raw/commented values
            data.append(item + " " + value + "\n")

    return "\n".join(map(lambda x: str(x), data))  # convert back to string


def comment(data, what):
    """
    Comments line containing `what` in string `data`.

    Args:
        data (str): Configuration file in string.
        what (str): Line which will be commented out.

    Returns:
        str: Configuration file with commented `what`.
    """
    data = data.splitlines()

    data = map(
        lambda x: "#" + x if x.strip().split() == what.split() else x,
        data
    )

    return "\n".join(data)


def _is_deb_system():
    """
    Badly written test whether the system is deb/apt based or not.
    """
    return os.path.exists("/etc/apt")


def main(args):
    pass


# Main program ================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="edeposit.amqp.antivirus ClamAV initializer.",
    )
    parser.add_argument(
        flag="-v",
        name="--verbose",
        help="Print debug messages.",
        action="store_true"
    )
    parser.add_argument(
        flag="-o",
        name="--overwrite",
        help="""Overwrite default configuration file. Don't worry, your original
                file will be stored in backup_.""",
        action="store_true"
    )
    parser.add_argument(
        flag="-c",
        name="--config",
        default=settings.CONF_FILE,
        help="Path to the configuration file. Default %s." % settings.CONF_FILE
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Logger set to debug level.")
    else:
        logger.setLevel(logging.INFO)

    main(args)
