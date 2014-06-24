from contextlib import closing

from httpy.client import HttpServerRequests
from procol.console import print_err_trace
import quecco
from requem.remote_queue.queue import remote_connections
from requem.commands.client import RemoteDatabasesClient

from requem.http.client import DatabaseHttpClient
from requem.remote_pool.pool import pool_manager_process
from requem.zeromq.client import DatabasesZeroMqClient
from tests import connections


def select_number(connection, number):
    try:
        with closing(connection.cursor()) as cursor:
            result = cursor.select('''select ?''', (number, ))
            return result
    except BaseException, e:
        print_err_trace()


def multi_process_connect():
    return connections['test'](scope=quecco.scope.processes)


def db_local_connection():
    return connections['test'](scope=quecco.scope.local)


def db_zero_mq_client():
    databases = DatabasesZeroMqClient('localhost', 9090)

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