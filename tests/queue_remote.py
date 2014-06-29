from procol.queue.manager import queue_client
from quelo.query import get_value
from requem.commands.client import RemoteDatabasesClient
from tests.connection import test_connection


def main():
    #Start server in servers/queue
    databases = RemoteDatabasesClient(queue_client(server_address=('127.0.0.1', 50000)))

    with databases.connect('test') as conn:
        with conn.cursor() as cursor:
            result = get_value(cursor, '''select 1''')
            assert 1 == result
            test_connection(cursor)


if __name__ == '__main__':
    main()