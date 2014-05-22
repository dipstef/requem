import cPickle as pickle
import sys

import web
from unicoder import encoded, to_unicode

from ..commands import IntraProcessDbCommands
from ..commands.connection import connection_tuple, cursor_tuple


urls = ('/database/(.+)/', 'DatabaseService',
        '/database/(.+)/conn/(\d+)', 'ConnectionService',
        '/database/(.+)/conn/(\d+)/cursor/(\d+)', 'CursorService')


app = web.application(urls, globals())


class DatabaseService(object):

    def GET(self, database):
        return databases.connect(database)


class ConnectionService(object):

    def GET(self, database, connection_id):
        return connections.cursor(connection_tuple(database, connection_id))

    def POST(self, database, connection_id):
        connections.commit(connection_tuple(database, connection_id))

    def DELETE(self, database, connection_id):
        connections.close(connection_tuple(database, connection_id))


class CursorService(object):

    def GET(self, database, connection_id, cursor_id):
        cursor = cursor_tuple(database, connection_id, cursor_id)
        query, args = query_data()

        result = cursors.select(cursor, query, args)
        return pickle.dumps(result)

    def POST(self, database, connection_id, cursor_id):
        cursor = cursor_tuple(database, connection_id, cursor_id)
        statement, args = query_data()

        result = cursors.execute(cursor, statement, args)
        return pickle.dumps(result)

    def DELETE(self, database, connection_id, cursor_id):
        cursor = cursor_tuple(database, connection_id, cursor_id)

        result = cursors.close(cursor)
        return pickle.dumps(result)


def query_data():
    query, args = _query_args()
    args = pickle.loads(encoded(args))

    args = tuple(to_unicode(arg) if isinstance(arg, basestring) else arg for arg in args)
    return query, args


def _query_args():
    user_data = web.input()
    query, args = user_data.query, user_data.args
    return query, args


def serve(db_connections, port):
    global databases, connections, cursors
    databases = IntraProcessDbCommands(db_connections)
    connections = databases.connections
    cursors = connections.cursors

    sys.argv = ['localhost']
    sys.argv.append(str(port))
    app.run()
    #After Keyboard Interrupt
    print 'Closing Connections'
    databases.close()
