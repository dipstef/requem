from tests.performance.serial.http import http_test

from tests.performance.serial.ipc import process_queue_test
from tests.performance.serial.local import local_test
from tests.performance.serial.manager import remote_queue_test, connection_manager_test
from tests.performance.serial.zero_mq import zero_mq_test


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