from base_db import BaseDbInterface


class MysqlDb(BaseDbInterface):

    # Stub example

    def __init__(self):
        pass

    def get(self, id, side):
        raise NotImplementedError('This is sample functionality')

    def save(self, id, side, data):
        raise NotImplementedError('This is sample functionality')
