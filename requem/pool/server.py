from .pool import pool_manager


def serve(connections, port=50001, local=True):
    host = '127.0.0.1' if local else '0.0.0.0'

    manager = pool_manager(connections, address=(host, port))
    server = manager.get_server()

    print 'Serving on port: ', port
    server.serve_forever()