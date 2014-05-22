from tests import connections

from requem.http.server import serve


def main():
    serve(connections, port=8086)

if __name__ == '__main__':
    main()