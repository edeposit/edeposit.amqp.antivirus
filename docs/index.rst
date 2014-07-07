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

Database update
^^^^^^^^^^^^^^^
You should update the signature database from time to time.

You can do it by running ``freshclam`` command, or by sending
:class:`.UpdateDatabase` structure over AMQP.

I think, that the best way is to put the ``freshclam`` command to cron.

Usage
-----

To check some file, encode it to ``base64``, put it into :class:`.ScanFile`
structure and send it over AMQP to :func:`.reactToAMQPMessage`.

Here is example without AMQP communication, but at the AMQP level of
abstraction::

    $ python
    >>> import base64
    >>> import antivirus as av
    >>> fn = "test_file.exe"
    >>> data = open(fn).read()
    >>> av.reactToAMQPMessage(
    ...    av.structures.ScanFile(fn, base64.b64encode(data)),
    ...    "UUID"
    ... )
    ScanResult(filename='test_file.exe', result={})  # result is blank -> file is ok

Or positive detection::

    $ python
    >>> import base64
    >>> import antivirus as av
    >>> fn = "eicar.com"
    >>> data = open(fn).read()
    >>> av.reactToAMQPMessage(
    ...    av.structures.ScanFile(fn, base64.b64encode(data)),
    ...    "UUID"
    ... )
    ScanResult(filename='test_file.exe', result={u'/tmp/tmpuCA2fe_eicar.com': ('FOUND', 'Eicar-Test-Signature')})

Content
-------
Parts of the module can be divided into two subcategories - script and API.

.. image:: /_static/relations.png


Standalone script
+++++++++++++++++

Script can be found in ``bin/`` folder and it should be automatically put into
your path, so you can just simply run ``edeposit_clamd_init.py`` from shell.

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
Test script expects that pytest_ is installed. In case you don't have it yet,
it can be easily installed using following command::

    pip install --user pytest

or for all users::

    sudo pip install pytest

.. _pytest: http://pytest.org/


Options
+++++++
Script provides three options - to run just unittests (``-u`` switch), to run
integration tests (``-i`` switch) or to run both (``-a`` switch).

Integration tests requires that ClamAV is installed, running and that the test
script has **root permissions**. 

Example of the success output from the test script::

    $ sudo service clamav-daemon start
    [sudo] password for bystrousak: 
     * Starting ClamAV daemon clamd

    $ ./run_tests.sh -a
    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.5 -- py-1.4.20 -- pytest-2.5.2
    collected 7 items 

    src/edeposit/amqp/antivirus/tests/integration/test_antivirus.py .....
    src/edeposit/amqp/antivirus/tests/unittests/test_amqp.py ..

    ========================== 7 passed in 44.04 seconds ===========================


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
