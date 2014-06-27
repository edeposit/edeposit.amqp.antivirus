edeposit.amqp.antivirus
=======================

This module provides wrappers over ClamAV_ antivirus for edeposit_ project.

.. _ClamAV: http://www.clamav.net/
.. _edeposit: http://edeposit.nkp.cz/

Installation
------------
Module is hosted at PIP, so you can install it easily with following command::

    sudo pip install edeposit.amqp.antivirus

This will install the module and necessary requirements with one exception
- the ClamAV itself. That can be installed manually or using package
manager from your distribution.

Ubuntu/Debian::

    sudo apt-get install clamav clamav-daemon

OpenSuse::

    sudo zypper install clamav

Initialization
++++++++++++++
After installation of the ``ClamAV`` and ``edeposit.amqp.antivirus``, run the
:doc:`edeposit_clamd_init.py </initializer>` script (should be in your path),
which will configure ClamAV and create all necessary files and directories.

You may also want to check :mod:`.settings` module, to change some of the paths
using JSON configuration files.

Usage
-----


TODO: fix

Content
-------
Parts of the module can be divided into two subcategories - script and API.


Standalone script
+++++++++++++++++
.. toctree::
    :maxdepth: 1

    /initializer


API
+++
.. toctree::
    :maxdepth: 1

    /api/antivirus
    /api/antivirus.antivirus
    /api/antivirus.structures
    /api/antivirus.settings
    /api/antivirus.wrappers


Source code
-----------
The project is opensource (GPL) and source codes can be found at GitHub:

- https://github.com/edeposit/edeposit.amqp.antivirus

Testing
-------
Almost every feature of the project is tested in unit/integration tests. You
can run this tests using provided ``run_tests.sh`` script, which can be found
in the root of the project.

Requirements
++++++++++++
This script expects that pytest_ is installed. In case you don't have it yet,
it can be easily installed using following command::

    pip install --user pytest

or for all users::

    sudo pip install pytest

.. _pytest: http://pytest.org/


Options
+++++++
Script provides three options - to run just unittests (``-u`` switch), to run
integration tests (``-i`` switch) or to run both (``-a`` switch).

Integration tests requires that ProFTPD is installed (there is test to test
this) and also **root permissions**. Integration tests are trying all usual
(and some unusual) use-cases, permissions to read/write into ProFTPD 
configuration files and so on. Thats why the root access is required.

Example of the success output from test script::

    $ ./run_tests.sh -a
    [sudo] password for bystrousak: 
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.5 -- py-1.4.20 -- pytest-2.5.2
    collected 42 items 

TODO: fix

    ========================== 42 passed in 13.96 seconds ==========================


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

 