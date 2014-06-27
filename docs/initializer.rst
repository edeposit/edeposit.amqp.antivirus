Initializer script
==================

.. automodule:: edeposit_clamd_init
    :members:
    :undoc-members:
    :show-inheritance:


Usage
-----

::

    $ ./edeposit_clamd_init.py -h
    usage: edeposit_clamd_init.py [-h] [-v] [-o] [-c CONFIG]

    edeposit.amqp.antivirus ClamAV initializer.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Print logging messages.
      -o, --overwrite       Overwrite default configuration file. Don't worry,
                            your original file will be stored in backup_.
      -c CONFIG, --config CONFIG
                            Path to the configuration file. Default
                            /etc/clamav/clamd.conf.