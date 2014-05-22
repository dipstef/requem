from collections import namedtuple


class DatabaseConnection(namedtuple('DatabaseConnection', ['database', 'id'])):

    def __new__(cls, database, connection_id):
        return super(DatabaseConnection, cls).__new__(cls, database, connection_id)


class DatabaseCursor(namedtuple('DatabaseCursor', ['connection', 'id'])):
    def __new__(cls, connection, cursor_id):
        return super(DatabaseCursor, cls).__new__(cls, connection, cursor_id)


def connection_tuple(database, connection_id):
    return DatabaseConnection(database, connection_id)


def cursor_tuple(database, connection_id, cursor_id):
    return DatabaseCursor(DatabaseConnection(database, connection_id), cursor_id)