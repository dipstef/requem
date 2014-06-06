from multiprocessing import Pool
import timeit
from tests.performance import select_number

conn = None


def select(number):
    global conn
    return select_number(conn, number)


def pool_execute(select_fun, processes=5, numbers=10, times=1):
    def _pool_test():
        pool = Pool(processes)
        result = pool.map(select_fun, xrange(1, numbers+1))

        pool.close()
        return result
    return timeit.timeit(_pool_test, number=times)


def pool_test(connection, processes=5, numbers=10, times=1):
    global conn
    conn = connection
    return pool_execute(select, processes, numbers, times)