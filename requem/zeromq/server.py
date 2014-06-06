"""Broker-less distributed task queue."""
import zmq

from ..commands import DbCommands
from requem.zeromq import context


class DatabaseWorker(object):

    def __init__(self, connections, port, local=False):
        self.host = '127.0.0.1' if local else '0.0.0.0'
        self.port = port
        self._socket = context.socket(zmq.REP)
        self._commands = DbCommands(connections)

    def start(self):
        self._socket.bind('tcp://{}:{}'.format(self.host, self.port))
        while True:
            command, args, kwargs = self._socket.recv_pyobj()

            response = self._commands.execute(command, *args, **kwargs)
            self._socket.send_pyobj(response)

    def close(self):
        self._socket.close()
        self._commands.close_connections()


def serve(connections, port, local=False):
    print 'Database Serving in', port
    db_service = DatabaseWorker(connections, port, local=local)
    try:
        db_service.start()
    except (KeyboardInterrupt, SystemExit):
        print 'Closing'
        db_service.close()