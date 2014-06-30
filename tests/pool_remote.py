from contextlib import closing

from quelo.query import get_value

from requem.pool import pool_client
from tests.connection import test_connection


def main():
    pool = pool_client(server_address=('127.0.0.1', 50001))

    connection = pool.connect('test')

    with closing(connection) as conn:
        cursor = conn.cursor()
        with closing(cursor) as cursor:
            assert 1 == get_value(cursor, '''select 1''')

            test_connection(cursor)

if __name__ == '__main__':
    main()