from tests.performance import db_zero_mq_client, select_number
from tests.performance.parallel import pool_execute


def zero_mq_test(processes=5, times=1):
    return pool_execute(_mq_select, processes=processes, times=times)


def _mq_select(number):
    with db_zero_mq_client() as mq_conn:
        return select_number(mq_conn, number)


def test_parallel(processes=5, times=100):
    print 'Zero Mq: ', zero_mq_test(processes, times=times)


def main():
    #test_parallel()
    test_parallel(processes=5, times=10)

if __name__ == '__main__':
    main()