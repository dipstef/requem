from procol.queue import ProducerConsumerThread
from procol.queue.remote_manager import queue_manager_process
from procol.queue.intra_processes import ProducerConsumer

from ..commands import DbCommands


class RemoteConnectionsQueue(ProducerConsumerThread):
    def __init__(self, connections):
        super(RemoteConnectionsQueue, self).__init__(ProducerConsumer)
        self._commands = DbCommands(connections)
        self.produce(produce_fun=self._produce)

    def _produce(self, command):
        return self._execute_command(*command)

    def _execute_command(self, command, args, kwargs):
        return self._commands.execute(command, *args, **kwargs)

    def execute(self, command, *args, **kwargs):
        return self._producer_consumer.execute((command, args, kwargs))

    def _done_requests(self):
        self.close()


def remote_connections(connections):
    return queue_manager_process(RemoteConnectionsQueue(connections))