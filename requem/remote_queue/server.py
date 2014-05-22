from procol.queue.remote_manager import queue_server
from .queue import RemoteConnectionsQueue


def serve(connections):
    return queue_server(RemoteConnectionsQueue(connections))