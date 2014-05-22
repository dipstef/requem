from quelo.query import get_value

from requem.zeromq.client import DatabasesZeroMqClient


def main():
    databases = DatabasesZeroMqClient('localhost', 9090)

    conn = databases.connect('test')

    cursor = conn.cursor()
    assert 1 == get_value(cursor, '''select 1''')

if __name__ == '__main__':
    main()