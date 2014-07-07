antivirus package
=================

There are two levels of abstraction - AMPQ API and python API.

AQMP API is higlevel API, where you send some structure, something happens
in magick box and you get back another structure.

Python API is just collection of `"lowlevel"` python wrappers over ClamAV.

AMQP API
--------

.. automodule:: antivirus
    :members:
    :undoc-members:
    :show-inheritance:

All AMQP communication structures can be found in :mod:`~antivirus.structures`
submodule.

.. image:: /_static/amqp.png

Python API
----------

.. toctree::
    :maxdepth: 1

    antivirus.antivirus
    antivirus.conf_writer


Wrappers
++++++++

.. toctree::
    :maxdepth: 1

    antivirus.wrappers
    antivirus.wrappers.clamd
    antivirus.wrappers.clamscan
    antivirus.wrappers.freshclam

Package configuration
---------------------

If you wish to change behavior or paths to some of the files, you can use
do it in :mod:`~antivirus.settings` submodule.