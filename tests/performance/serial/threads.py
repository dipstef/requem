from tests.performance import multi_threads_connect
from tests.performance.serial import serial_test


def threads_queue_test(times=1):
    with multi_threads_connect() as conn:
        return serial_test(conn, times=times)


def test_serial(times=1):
    print 'Threads Queue:', threads_queue_test(times=times)


def main():
    test_serial(times=100)

if __name__ == '__main__':
    main()