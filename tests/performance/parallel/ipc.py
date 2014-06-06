from tests.performance import multi_process_connect
from tests.performance.parallel import pool_test


def process_queue_test(processes=5, times=1):
    with multi_process_connect() as conn:
        return pool_test(conn, processes=processes, times=times)


def test_parallel(processes=5, times=100):
    print 'Process Queue', process_queue_test(processes, times=times)


def main():
    #test_parallel()
    test_parallel(processes=5, times=10)

if __name__ == '__main__':
    main()