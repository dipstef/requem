from procol.queue.remote_manager import queue_client
from quelo.query import get_value
from requem.commands.client import RemoteDatabasesClient


def main():
    #Start server in servers/queue
    databases = RemoteDatabasesClient(queue_client(server_address=('127.0.0.1', 50000)))

    conn = databases.connect('test')

    cursor = conn.cursor()
    assert 1 == get_value(cursor, '''select 1''')

if __name__ == '__main__':
    main()