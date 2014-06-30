from tests.performance import db_zero_mq_client, db_zero_mq_local_client
from tests.performance.serial import serial_test


def zero_mq_test(times=1):
    with db_zero_mq_client() as conn:
        return serial_test(conn, times=times)


def zero_mq_local_test(times=1):
    with db_zero_mq_local_client() as conn:
        return serial_test(conn, times=times)


def test_serial(times=1):
    print 'Zero Mq: ', zero_mq_test(times=times)
    print 'Zero Mq Local: ', zero_mq_local_test(times=times)


def main():
    test_serial(times=100)

if __name__ == '__main__':
    main()