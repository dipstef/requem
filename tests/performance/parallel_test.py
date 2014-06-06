from tests.performance.parallel.http import http_test
from tests.performance.parallel.ipc import process_queue_test
from tests.performance.parallel.manager import remote_queue_test, connection_manager_test
from tests.performance.parallel.zero_mq import zero_mq_test


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