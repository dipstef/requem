import timeit
from tests.performance import select_number


def serial_test(conn, numbers=10, times=1):
    def _serial_test():
        for i in xrange(1, numbers + 1):
            r = select_number(conn, i)

    return timeit.timeit(_serial_test, number=times)