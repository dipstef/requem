from httpy.client import HttpServerRequests
from quelo.query import get_value

from requem.http.client import DatabaseHttpClient
from tests.connection import test_connection


def main():
    client = HttpServerRequests(('localhost', 8086))

    databases = DatabaseHttpClient(client)

    with databases.connect('test') as conn:
        with conn.cursor() as cursor:
            assert 1 == get_value(cursor, '''select 1''')
            test_connection(cursor)

if __name__ == '__main__':
    main()