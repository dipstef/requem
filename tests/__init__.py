import os
import quecco

_db = os.path.join(os.path.dirname(__file__), 'test.db')
_init_file = os.path.join(os.path.dirname(__file__), 'test.sql')


def _connect(scope=quecco.local):
    return scope(_db, init_file=_init_file)


connections = {'test': _connect}