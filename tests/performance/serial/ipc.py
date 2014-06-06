from tests.performance import multi_process_connect
from tests.performance.serial import serial_test


def process_queue_test(times=1):
    with multi_process_connect() as conn:
        return serial_test(conn, times=times)


def test_serial(times=1):
    print 'Process Queue:', process_queue_test(times=times)


def main():
    test_serial(times=100)

if __name__ == '__main__':
    main()