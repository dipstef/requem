Requem
======

Allows to query a ``sqlite3`` database hosted remotely.
This by no means substitutes the need of using a RDBMS but provides basic query functionalities, and is a temporary
solution for transitioning to a database server while your application is growing to a multi-host deployment.

As ``requem`` is built on top ``quecco``: https://github.com/dipstef/quecco, database performance is limited by
the underlying producer-consumer queue implementation (which allows only the thread creating the connection to execute
statements), however there are interesting figures regarding which technology is being exposed to establish remote
communication.
The ``zeromq`` based implementation seems to hold the best performance.

Usage
=====
Same interace as ``quelo``: https://github.com/dipstef/quelo

Create connections for available databases

.. code-block:: python

    def _connect(scope=quecco.local):
        return quecco.connect('test.db', scope=threads, init_file='test.sql')

    connections = {'test': _connect}

ZeroMq server:

.. code-block:: python

    from requem.zeromq import server

    >>> server.serve(connections, port=9090)


ZeroMq client:

.. code-block:: python

    from requem.zeromq.client import DatabasesZeroMqClient

    >>> databases = DatabasesZeroMqClient('server-address', 9090)

    with databases.connect('test') as conn:
        ....

Remote queue through trough ``multiprocessing`` managers

.. code-block:: python

    from requem.queue.server import serve

Remote queue client

.. code-block:: python

    from procol.queue.manager import queue_client
    from requem.commands.client import RemoteDatabasesClient

    >>> RemoteDatabasesClient(queue_client(server_address=('127.0.0.1', 50000)))

Other options are available just for the sake of comparison, which are not necessary suitable for this sort of
problem.

Performance
===========
For the sake of comparison

executing 100 times:

.. code-block:: sql
    select 1


================Local===============
Single Connection:   0.0456030368805
Threads Queue:       0.945885896683
Process Queue:       0.977910041809
Zero Mq:             1.28202390671
===============Remote===============
Zero Mq:             1.36838197708
Remote Queue:        1.65378189087
Http:                94.9913551807

The http interface running on ``web.py`` relies in threads based producer consumer queue as every http request
is handled by a new thread.
Using a more performant web server might hold better results, as well there exists better approaches to handle
this scenario,  as using``SQLAlchemy``.

The ``zeromq`` solution seems to offer the best compromise.