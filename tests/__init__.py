import atexit
import os

import quecco


class TestDatabaseConnection(object):

    def __init__(self):
        self._path = os.path.join(os.path.dirname(__file__), 'test.db')
        atexit.register(self._remove_path)

    def __call__(self, scope=quecco.scope.local):
        return quecco.connect(self._path, scope=scope)

    def __exit__(self, *args):
        self._remove_path()

    def _remove_path(self):
        if os.path.exists(self._path):
            os.remove(self._path)


connections = {'test': TestDatabaseConnection()}