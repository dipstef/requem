import cPickle as pickle
from contextlib import closing

from unicoder import encoded

from .urls import database_url, database_connection_url, database_cursor_url


class ResponseBodyClient():
    def __init__(self, client):
        self._client = client

    def get(self, url, **params):
        response = self._client.get(url, timeout=None, params=params)
        return response.body

    def post(self, url, **params):
        response = self._client.post(url, timeout=None, params=params)
        return response.body

    def delete(self, url, **params):
        response = self._client.delete(url, timeout=None, params=params)
        return response.body


class DatabaseHttpClient(object):
    def __init__(self, server_client):
        self._client = ResponseBodyClient(server_client)
        self._connections_urls = {}
        self._cursor_urls = {}

    def connect(self, database):
        connection_id = int(self._client.get(database_url(database)))

        return DatabaseHttpConnection(database, connection_id, self._client)


class DatabaseHttpConnection(closing):
    def __init__(self, database, connection_id, client):
        super(DatabaseHttpConnection, self).__init__(self)
        self._client = client
        self._database = database
        self._connection_id = connection_id
        self._connection_path = database_connection_url(database, connection_id)

    def cursor(self):
        cursor_id = int(self._client.get(self._connection_path))

        return DatabaseHttpCursor(self._database, self._connection_id, cursor_id, self._client)

    def commit(self):
        return self._client.post(self._connection_path)

    def close(self):
        pass


class DatabaseHttpCursor(closing):
    def __init__(self, database, connection_id, cursor_id, client):
        super(DatabaseHttpCursor, self).__init__(self)
        self._client = client
        self._cursor_path = database_cursor_url(database, connection_id, cursor_id)

    def select(self, query, args=()):
        body = self._client.get(self._cursor_path, query=query, args=_encode(args))
        return _load(body)

    def execute(self, query, args=()):
        body = self._client.post(self._cursor_path, query=query, args=_encode(args))
        return _load(body)

    def close(self):
        body = self._client.delete(self._cursor_path)
        return _load(body)


def _encode(args):
    return pickle.dumps(_encoded_tuple(args if args else ()))


def _encoded_tuple(args):
    return tuple(encoded(arg) if isinstance(arg, unicode) else arg for arg in args)


def _load(body):
    result = pickle.loads(body)
    if isinstance(result, BaseException):
        raise result
    return result