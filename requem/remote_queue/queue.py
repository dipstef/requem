from procol.queue import ProducerThread
from procol.queue.manager import queue_manager_process
from procol.queue.ipc import ProducerConsumer

from ..commands import DbCommands


class RemoteConnectionsQueue(ProducerThread):
    def __init__(self, connections):
        super(RemoteConnectionsQueue, self).__init__(ProducerConsumer, producer=self._produce)
        self._commands = DbCommands(connections)

    def _produce(self, command):
        return self._execute_command(*command)

    def _execute_command(self, command, args, kwargs):
        return self._commands.execute(command, *args, **kwargs)

    def execute(self, command, *args, **kwargs):
        result = super(RemoteConnectionsQueue, self).execute((command, args, kwargs))
        if isinstance(result, BaseException):
            raise result
        return result

    def _done_requests(self):
        self.close()


def remote_connections(connections):
    return queue_manager_process(RemoteConnectionsQueue(connections))