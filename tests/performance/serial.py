import timeit

from tests.performance import select_number, multi_process_connect, db_zero_mq_client, db_http_client, \
    pool_manager_connection, db_local_connection, db_remote_queue


def serial_test(conn, numbers=10, times=1):
    def _serial_test():
        for i in xrange(1, numbers + 1):
            r = select_number(conn, i)

    return timeit.timeit(_serial_test, number=times)


def local_test(times=1):
    with db_local_connection() as conn:
        return serial_test(conn, times=times)


def process_queue_test(times=1):
    with multi_process_connect() as conn:
        return serial_test(conn, times=times)


def zero_mq_test(times=1):
    with db_zero_mq_client() as conn:
        return serial_test(conn, times=times)


def remote_queue_test(times=1):
    with db_remote_queue() as conn:
        return serial_test(conn, times=times)


def http_test(times=1):
    with db_http_client() as conn:
        return serial_test(conn, times=times)


def connection_manager_test(times=1):
    conn = pool_manager_connection()
    result = serial_test(conn, times=times)
    conn.close()
    return result


def test_serial(times=1):
    print 'Local:', local_test(times=times)
    print
    print 'Process Queue:', process_queue_test(times=times)
    print
    print 'Zero Mq: ', zero_mq_test(times=times)
    print
    print 'Remote Queue: ', remote_queue_test(times=times)
    print
    print 'Http: ', http_test(times=times)
    print
    print 'Connection Manager:', connection_manager_test(times=times)


def main():
    test_serial(times=100)

if __name__ == '__main__':
    main()