from tests.performance import db_remote_queue, pool_manager_connection
from tests.performance.parallel import pool_test


def remote_queue_test(processes=5, times=1):
    with db_remote_queue() as conn:
        return pool_test(conn, processes=processes, times=times)


def connection_manager_test(processes=5, times=1):
    conn = pool_manager_connection()
    result = pool_test(conn, processes=processes, times=times)
    conn.close()
    return result


def test_parallel(processes=5, times=100):
    print 'Remote Queue: ', remote_queue_test(processes, times=times)
    print
    print 'Connection Manager:', connection_manager_test(processes, times=times)


def main():
    #test_parallel()
    test_parallel(processes=5, times=10)


if __name__ == '__main__':
    main()
