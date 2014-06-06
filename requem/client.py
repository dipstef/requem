from contextlib import closing


class DatabaseClient(object):

    def __init__(self, client):
        self._databases_client = client

    def connection(self, database):
        connection_client = self._databases_client.connect(database)

        return ConnectionClient(connection_client)


class ConnectionClient(closing):
    def __init__(self, connection_client):
        super(ConnectionClient, self).__init__(self)
        self._connection_client = connection_client
        self._cursors = []

    def cursor(self):
        cursor_client = self._connection_client.cursor()

        cursor = CursorClient(cursor_client)
        self._cursors.append(cursor)
        return cursor

    def commit(self):
        self._connection_client.commit()

    def close(self):
        self._connection_client.close()
        for cursor in self._cursors:
            if not cursor.is_closed():
                cursor.close()


class CursorClient(closing):

    def __init__(self, cursor_client):
        super(CursorClient, self).__init__(self)
        self._cursor_client = cursor_client
        self._closed = False

    def execute(self, query, args=()):
        result = self._cursor_client.execute(query, args=args)
        return _parse_result(result)

    def select(self, query, args=()):
        result = self._cursor_client.select(query, args=args)

        return _parse_result(result)

    def close(self):
        self._cursor_client.close()
        self._closed = True

    def is_closed(self):
        return self._closed


def _parse_result(result):
    if isinstance(result, Exception):
        raise result
    else:
        return result