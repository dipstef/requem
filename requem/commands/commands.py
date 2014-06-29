from procol.console import print_err_trace
import quecco

from quelo.error import DbError, ClosedCursor
from quecco.process.connections import CursorNotFound, DbConnections


class DatabasesCommands(object):
    def __init__(self, db_connections, scope=quecco.local):
        self._databases = DbConnections(db_connections)
        self.connections = ConnectionCommands(self)
        self._connection_scope = scope

    def connect(self, database, **kwargs):
        conn = self._databases.connect(database, scope=self._connection_scope, **kwargs)
        return conn.id

    def get_connection(self, connection):
        return self._databases.get_connection(connection.database, connection.id)

    def close(self):
        self._databases.close()


class ConnectionCommands(object):
    def __init__(self, database_connections):
        self._databases = database_connections
        self.cursors = CursorCommands(self)

    def cursor(self, connection):
        conn = self._databases.get_connection(connection)
        return conn.create_cursor()

    def commit(self, connection):
        conn = self._databases.get_connection(connection)
        conn.commit()

    def close(self, connection):
        self._databases.close(connection.database, connection.id)

    def get_cursor(self, cursor):
        conn = self._databases.get_connection(cursor.connection)

        return conn.get_cursor(cursor.id)

    def close_cursor(self, cursor):
        conn = self._databases.get_connection(cursor.connection)

        conn.close_cursor(cursor.id)


class CursorCommands(object):

    def __init__(self, database_connections):
        self._connections = database_connections

    def select(self, cursor, query, args):
        try:
            cursor = self._connections.get_cursor(cursor)

            result = cursor.select(query, args)

            return result
        except DbError, e:
            print_err_trace()
            return e
        except CursorNotFound:
            return ClosedCursor(query, args)

    def execute(self, cursor, statement, args):
        try:
            cursor = self._connections.get_cursor(cursor)

            result = cursor.execute(statement, args)
            return result
        except DbError, e:
            return e
        except CursorNotFound:
            return ClosedCursor(statement, args)

    def close(self, cursor):
        try:
            self._connections.close_cursor(cursor)
        except CursorNotFound, e:
            return e

