from multiprocessing import Pool
import timeit
from tests.performance import select_number, multi_process_connect, pool_manager_connection, db_http_client, \
    db_zero_mq_client, db_remote_queue


def select(number):
    global conn
    return select_number(conn, number)

conn = None


def pool_test(processes=5, select_fun=select, numbers=10, times=1):
    def _pool_test():
        pool = Pool(processes)
        result = pool.map(select_fun, xrange(1, numbers+1))

        pool.close()
        return result
    return timeit.timeit(_pool_test, number=times)


def process_queue_test(processes=5, times=1):
    global conn
    with multi_process_connect() as conn:
        return pool_test(processes=processes, times=times)


def zero_mq_test(processes=5, times=1):
    return pool_test(processes=processes, select_fun=_mq_select, times=times)


def _mq_select(number):
    with db_zero_mq_client() as mq_conn:
        return select_number(mq_conn, number)


def remote_queue_test(processes=5, times=1):
    global conn
    with db_remote_queue() as conn:
        return pool_test(processes=processes, select_fun=_mq_select, times=times)


def http_test(processes=5, times=1):
    global conn
    with db_http_client() as conn:
        return pool_test(processes=processes, times=times)


def connection_manager_test(processes=5, times=1):
    global conn
    conn = pool_manager_connection()
    result = pool_test(processes=processes, times=times)
    conn.close()
    return result


def test_parallel(processes=5, times=100):
    print 'Process Queue', process_queue_test(processes, times=times)
    print
    print 'Zero Mq: ', zero_mq_test(processes, times=times)
    print
    print 'Remote Queue: ', remote_queue_test(processes, times=times)
    print
    print 'Http: ', http_test(processes, times=times)
    print
    print 'Connection Manager:', connection_manager_test(processes, times=times)


def main():
    #test_parallel()
    test_parallel(processes=5, times=10)

if __name__ == '__main__':
    main()