from contextlib import closing
from .connection import cursor_tuple, connection_tuple
from . import DatabaseCommand


class RemoteDatabasesClient(object):

    def __init__(self, client):
        self._client = client
        self._connections_urls = {}
        self._cursor_urls = {}

    def connect(self, database):
        connection_id = self._client.execute(DatabaseCommand.CONN, database)

        return RemoteConnectionClient(connection_tuple(database, connection_id), self._client)


class RemoteConnectionClient(closing):
    def __init__(self, connection, client):
        super(RemoteConnectionClient, self).__init__(self)
        self._connection = connection
        self._client = client

    def cursor(self):
        cursor_id = self._client.execute(DatabaseCommand.CONN_CURSOR, self._connection)

        cursor = cursor_tuple(self._connection.database, self._connection.id, cursor_id)
        return RemoteCursorClient(cursor, self._client)

    def commit(self):
        return self._client.execute(DatabaseCommand.CONN_COMMIT, self._connection)

    def close(self):
        self._client.close()


class RemoteCursorClient(closing):
    def __init__(self, cursor, client):
        super(RemoteCursorClient, self).__init__(self)
        self._cursor = cursor
        self._client = client

    def select(self, query, args=()):
        return self._client.execute(DatabaseCommand.CURSOR_SELECT, self._cursor, query, args)

    def execute(self, query, args=()):
        return self._client.execute(DatabaseCommand.CURSOR_EXECUTE, self._cursor, query, args)

    def close(self):
        return self._client.execute(DatabaseCommand.CURSOR_CLOSE, self._cursor)