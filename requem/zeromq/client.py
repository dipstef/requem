from ..client import DatabaseClient
from ..commands.client import RemoteDatabasesClient
import zmq


class ZeroMqClient(object):

    def __init__(self, host, port):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect('tcp://{}:{}'.format(host, port))

    def execute(self, command, *args, **kwargs):
        self._socket.send_pyobj((command, args, kwargs))

        result = self._socket.recv_pyobj()
        if isinstance(result, BaseException):
            raise result
        return result

    def close(self):
        self._socket.close()


class DatabasesZeroMqClient(RemoteDatabasesClient):
    def __init__(self, host, port):
        super(DatabasesZeroMqClient, self).__init__(ZeroMqClient(host, port))


class ZeroMqDatabaseClient(DatabaseClient):
    def __init__(self, host, port):
        super(ZeroMqDatabaseClient, self).__init__(DatabasesZeroMqClient(host, port))