from requem.remote_queue.server import serve
from tests import connections


def main():
    serve(connections)

if __name__ == '__main__':
    main()