#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import sh
import pwd
import sys
import shutil
import os.path
import logging
import argparse


try:
    import edeposit.amqp.antivirus as antivirus
    from edeposit.amqp.antivirus import settings
    from edeposit.amqp.antivirus import conf_writer
    from edeposit.amqp.antivirus.wrappers.freshclam import require_root
except ImportError:
    sys.path.insert(0, os.path.abspath('../src/edeposit/amqp'))
    import antivirus
    from antivirus import settings
    from antivirus import conf_writer
    from antivirus.wrappers.freshclam import require_root


# Variables ===================================================================
logging.basicConfig()
logger = logging.getLogger(__name__)

#: All required settings is there, rest is not important.
REQUIRED_SETTINGS = {
    "User": "$username",
    "LocalSocketGroup": "$groupname",
    "LocalSocket": settings.LOCALSOCKET,
    "LogFile": settings.LOGFILE,
    "PidFile": settings.PIDFILE,
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


# base64 encoded zlib compressed string
CLEAN_CONFIG = """
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
ojrs
"""

# decode compressed clean config
import zlib
import base64
CLEAN_CONFIG = zlib.decompress(base64.b64decode(CLEAN_CONFIG))


# Functions & objects =========================================================
def get_username():
    if settings.is_deb_system():
        return "clamav"
    else:
        return "vscan"


def update_configuration(configuration):
    for key, val in REQUIRED_SETTINGS.items():
        if val in ["$username", "$groupname"]:
            val = get_username()

        configuration = conf_writer.add_or_update(configuration, key, val)

    return configuration


def create_config(cnf_file, uid, overwrite):
    conf = None

    # needed also on suse, because pyClamd module
    if not os.path.exists(settings.DEB_CONF_PATH):
        os.makedirs(settings.DEB_CONF_PATH, 0755)
        os.chown(settings.DEB_CONF_PATH, uid, -1)

    if not os.path.exists(cnf_file):       # create new conf file
        conf = CLEAN_CONFIG
    elif overwrite:                        # ovewrite old conf file
        backup_name = cnf_file + "_"
        if not os.path.exists(backup_name):
            shutil.copyfile(cnf_file, backup_name)
            os.chown(backup_name, uid, -1)

        conf = CLEAN_CONFIG
    else:                                  # switch variables in existing file
        with open(cnf_file) as f:
            conf = f.read()

    # write the conf file
    with open(cnf_file, "w") as f:
        f.write(update_configuration(conf))

    # permission check (uid)
    os.chown(cnf_file, uid, -1)
    os.chmod(cnf_file, 0644)

    if not settings.is_deb_system():
        symlink = settings.DEB_CONF_PATH + settings.CONF_FILE
        os.symlink(cnf_file, symlink)
        os.chown(symlink, uid, -1)
        os.chmod(symlink, 0644)


def create_log(log_file, uid):
    if not os.path.exists(log_file):  # create new log file
        dir_name = os.path.dirname(log_file)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, 0755)
            os.chown(dir_name, uid, -1)

        with open(log_file, "w") as f:
            f.write("")

    os.chown(log_file, uid, -1)
    os.chmod(log_file, 0640)


def get_service_name():
    if settings.is_deb_system():
        return "clamav-daemon"
    else:
        return "clamd"


@require_root
def main(conf_file, overwrite):
    uid = pwd.getpwnam(get_username()).pw_uid

    # stop the daemon
    sh.service(get_service_name(), "stop")

    # create files
    create_config(
        cnf_file=conf_file,
        uid=uid,
        overwrite=overwrite
    )
    create_log(
        log_file=REQUIRED_SETTINGS["LogFile"],
        uid=uid
    )

    # start the daemon
    sh.service(get_service_name(), "start")


# Main program ================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="edeposit.amqp.antivirus ClamAV initializer.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print debug messages.",
        action="store_true"
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        help="""Overwrite default configuration file. Don't worry, your original
                file will be stored in backup_.""",
        action="store_true"
    )
    parser.add_argument(
        "-c",
        "--config",
        default=settings.CONF_PATH,
        help="Path to the configuration file. Default %s." % settings.CONF_PATH
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Logger set to debug level.")
    else:
        logger.setLevel(logging.INFO)

    try:
        main(args.config, args.overwrite)
    except AssertionError as e:
        sys.stderr.write(e.message + "\n")
        sys.exit(1)
