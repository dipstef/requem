from requem.zeromq.server import serve
from tests import connections


def main():
    serve(connections, port=9090)

if __name__ == '__main__':
    main()