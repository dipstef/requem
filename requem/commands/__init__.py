from collections import namedtuple
import quecco
from .commands import DatabasesCommands


class DatabaseCommand(object):
    CONN, CONN_CURSOR, CONN_COMMIT, CONN_CLOSE, CONN_EXECUTE, CURSOR_EXECUTE, CURSOR_SELECT, CURSOR_CLOSE = range(8)


class DbCommands(object):

    def __init__(self, db_connections, scope=quecco.local):
        databases = DatabasesCommands(db_connections, scope)

        commands = {DatabaseCommand.CONN: databases.connect,
                    DatabaseCommand.CONN_CURSOR: databases.connections.cursor,
                    DatabaseCommand.CONN_COMMIT: databases.connections.commit,
                    DatabaseCommand.CONN_CLOSE: databases.connections.close,
                    DatabaseCommand.CURSOR_EXECUTE: databases.connections.cursors.execute,
                    DatabaseCommand.CURSOR_SELECT: databases.connections.cursors.select,
                    DatabaseCommand.CURSOR_CLOSE: databases.connections.cursors.close}

        self._commands = commands
        self._databases = databases

    def execute(self, command, *args, **kwargs):
        db_command = self._commands[command]
        return db_command(*args, **kwargs)

    def close_connections(self):
        self._databases.close()


class InProcessDbCommands(DatabasesCommands):

    def __init__(self, db_connections):
        super(InProcessDbCommands, self).__init__(db_connections, quecco.threads)


class DatabaseExecute(namedtuple('DatabaseExecute', ['command', 'args', 'kwargs'])):

    def __new__(cls, command, args, kwargs):
        return super(DatabaseExecute, cls).__new__(cls, command, args, kwargs)