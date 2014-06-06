from tests.performance import db_remote_queue, pool_manager_connection
from tests.performance.serial import serial_test


def remote_queue_test(times=1):
    with db_remote_queue() as conn:
        return serial_test(conn, times=times)


def connection_manager_test(times=1):
    conn = pool_manager_connection()
    result = serial_test(conn, times=times)
    conn.close()
    return result


def test_serial(times=1):
    print 'Remote Queue: ', remote_queue_test(times=times)
    print
    print 'Connection Manager:', connection_manager_test(times=times)


def main():
    test_serial(times=100)

if __name__ == '__main__':
    main()