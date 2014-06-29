from contextlib import closing
from quelo.query import get_value

from requem.zeromq.client import DatabasesZeroMqClient
from tests.connection import test_connection


def main():
    databases = DatabasesZeroMqClient('localhost', 9090)

    with databases.connect('test') as conn:
        with conn.cursor() as cursor:
            assert 1 == get_value(cursor, '''select 1''')

            test_connection(cursor)

if __name__ == '__main__':
    main()