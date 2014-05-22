from quelo.query import get_value
from requem.commands.client import RemoteDatabasesClient
from requem.remote_queue.queue import remote_connections
from tests import connections


def main():
    databases = RemoteDatabasesClient(remote_connections(connections))

    conn = databases.connect('test')

    cursor = conn.cursor()
    assert 1 == get_value(cursor, '''select 1''')

    conn.close()

if __name__ == '__main__':
    main()