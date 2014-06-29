from quelo.query import get_value
from requem.commands.client import RemoteDatabasesClient
from requem.remote_queue.queue import remote_connections
from tests import connections
from tests.connection import test_connection


def main():
    databases = RemoteDatabasesClient(remote_connections(connections))

    with databases.connect('test') as conn:
        with conn.cursor() as cursor:
            result = get_value(cursor, '''select 1''')
            assert 1 == result
            test_connection(cursor)

if __name__ == '__main__':
    main()