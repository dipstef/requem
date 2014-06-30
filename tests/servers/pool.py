from requem.pool.server import serve
from tests import connections


def main():
    serve(connections)

if __name__ == '__main__':
    main()