import multiprocessing
from multiprocessing.managers import SyncManager

from procol.queue import ProducerThread

from procol.queue.ipc import ProducerConsumer
import quecco


class ConnectionsPool(object):

    def __init__(self, db_connections):
        self._lock = multiprocessing.RLock()
        self._connections = db_connections
        self._connections_dict = {}

    def connect(self, database_name, **kwargs):
        with self._lock:
            connection = self._get_connection(database_name)
            if not connection:
                connection = self._connect(database_name, **kwargs)

            return connection

    def _connect(self, database_name, **kwargs):
        connection_fun = self._connections[database_name]

        connection = connection_fun(scope=quecco.ipc)
        self._connections_dict[database_name] = connection
        return connection

    def _get_connection(self, database_name):
        with self._lock:
            return self._connections_dict.get(database_name)


class PoolManagerThread(ProducerThread):

    def __init__(self, connections):
        super(PoolManagerThread, self).__init__(ProducerConsumer, producer=self._produce)
        self._pool = ConnectionsPool(connections)
        self.start()

    def _produce(self, command):
        return self._create_connection(*command)

    def _create_connection(self, database_name, connection_args):
        connection = self._pool.connect(database_name, **connection_args)

        connection = connection_proxy(connection)
        return connection

    def connect(self, database_name, **connection_args):
        return self.execute((database_name, connection_args))


class ConnectionsPoolManager(SyncManager):
        pass


def pool_manager(pool, address=None):
    _pool_manager = ConnectionsPoolManager(address=address, authkey='123456')

    pool = PoolManagerThread(pool)

    ConnectionsPoolManager.register('get_pool', callable=lambda: pool)

    return _pool_manager


def pool_manager_process(pool):
    _pool_manager = pool_manager(pool)

    _pool_manager.start()

    return _pool_manager.get_pool()


def connection_manager(connection, auth_key=None):
    class ConnectionManager(SyncManager):
        pass

    conn = ConnectionProxy(connection)
    ConnectionManager.register('get_connection', callable=lambda: conn)
    #auth_key = auth_key or multiprocessing.current_process().authkey

    manager = ConnectionManager(authkey=auth_key)
    manager.start()

    return manager


def connection_proxy(connection, auth_key=None):
    manager = connection_manager(connection, auth_key)

    return manager.get_connection()


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