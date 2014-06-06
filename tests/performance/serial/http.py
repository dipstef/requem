from tests.performance import db_http_client
from tests.performance.serial import serial_test


def http_test(times=1):
    with db_http_client() as conn:
        return serial_test(conn, times=times)


def test_serial(times=1):
    print 'Http: ', http_test(times=times)


def main():
    test_serial(times=100)

if __name__ == '__main__':
    main()