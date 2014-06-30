import multiprocessing
from multiprocessing.managers import SyncManager

from procol.queue import ProducerThread

from procol.queue.ipc import ProducerConsumer
import quecco

from .connection import connection_proxy


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
        result = self.execute((database_name, connection_args))
        if isinstance(result, BaseException):
            raise result
        return result


class ConnectionsPoolManager(SyncManager):
        pass


def pool_manager(connections, address=None):
    manager = ConnectionsPoolManager(address=address, authkey='123456')

    pool = PoolManagerThread(connections)

    ConnectionsPoolManager.register('get_pool', callable=lambda: pool)

    return manager


def pool_manager_process(connections):
    manager = pool_manager(connections)

    manager.start()

    return manager.get_pool()


def pool_client(server_address=None):
    ConnectionsPoolManager.register('get_pool')

    queue = ConnectionsPoolManager(address=server_address, authkey='123456')
    queue.connect()

    pool = queue.get_pool()

    return pool
