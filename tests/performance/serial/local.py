from tests.performance import db_local_connection
from tests.performance.serial import serial_test


def local_test(times=1):
    with db_local_connection() as conn:
        return serial_test(conn, times=times)


def test_serial(times=1):
    print 'Local:', local_test(times=times)


def main():
    test_serial(times=100)

if __name__ == '__main__':
    main()