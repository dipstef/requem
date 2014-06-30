from multiprocessing.managers import SyncManager


def connection_proxy(connection, auth_key=None):
    manager = connection_manager(connection, auth_key)

    return manager.get_connection()


def connection_manager(connection, auth_key=None):
    class ConnectionManager(SyncManager):
        pass

    conn = ConnectionProxy(connection)
    ConnectionManager.register('get_connection', callable=lambda: conn)
    #auth_key = auth_key or multiprocessing.current_process().authkey

    manager = ConnectionManager(authkey=auth_key)
    manager.start()

    return manager


class ConnectionProxy(object):
    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        cursor = cursor_manager(self._conn.cursor())
        return cursor

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


def cursor_manager(cursor, auth_key=None):
    class CursorManager(SyncManager):
        pass

    CursorManager.register('cursor', callable=lambda: cursor)

    #auth_key = auth_key or multiprocessing.current_process().authkey

    manager = CursorManager(authkey=auth_key)
    manager.start()
    proxy = manager.cursor()
    return proxy