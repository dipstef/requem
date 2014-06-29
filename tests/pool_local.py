from contextlib import closing
from quelo.query import get_value
from requem.remote_pool.pool import pool_manager_process
from tests import connections
from tests.connection import test_connection


def main():
    pool = pool_manager_process(connections)
    connection = pool.connect('test')

    with closing(connection) as conn:
        cursor = conn.cursor()
        with closing(cursor) as cursor:
            assert 1 == get_value(cursor, '''select 1''')

            test_connection(cursor)

if __name__ == '__main__':
    main()