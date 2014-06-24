from httpy.client import HttpServerRequests
from quelo.query import get_value

from requem.http.client import DatabaseHttpClient


def main():
    client = HttpServerRequests(('localhost', 8086))

    databases = DatabaseHttpClient(client)

    conn = databases.connect('test')

    cursor = conn.cursor()
    assert 1 == get_value(cursor, '''select 1''')

if __name__ == '__main__':
    main()