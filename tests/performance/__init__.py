from contextlib import closing

from httpy.client import HttpServerRequests
from procol.console import print_err_trace
import quecco
from quelo import get_value
from requem.queue import remote_connections
from requem.commands.client import RemoteDatabasesClient

from requem.http.client import DatabaseHttpClient
from requem.pool import pool_manager_process
from requem.zeromq.client import DatabasesZeroMqClient
from tests import connections


def select_number(connection, number):
    try:
        with closing(connection.cursor()) as cursor:
            result = get_value(cursor, '''select ?''', (number, ))
            return result
    except BaseException, e:
        print_err_trace()


def multi_threads_connect():
    connection = connections['test']
    return connection(scope=quecco.threads)


def multi_process_connect():
    connection = connections['test']
    return connection(scope=quecco.ipc)


def db_local_connection():
    connection = connections['test']
    return connection(scope=quecco.local)


def db_zero_mq_client():
    databases = DatabasesZeroMqClient('localhost', 9090)

    return databases.connect('test')


def db_zero_mq_local_client():
    databases = DatabasesZeroMqClient('127.0.0.1', 9091)

    return databases.connect('test')


def db_remote_queue():
    databases = RemoteDatabasesClient(remote_connections(connections))

    conn = databases.connect('test')
    return conn


def db_http_client():
    client = HttpServerRequests(('localhost', 8086))

    databases = DatabaseHttpClient(client)

    return databases.connect('test')


def pool_manager_connection():
    pool = pool_manager_process(connections)
    return pool.connect('test')