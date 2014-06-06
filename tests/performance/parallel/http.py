from tests.performance import db_http_client
from tests.performance.parallel import pool_test


def http_test(processes=5, times=1):
    with db_http_client() as conn:
        return pool_test(conn, processes=processes, times=times)