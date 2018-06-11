class BaseDbInterface(object):
    # this is interface that should be implemented instasnce of db storage

    def save(self, id, side, data):
        raise NotImplementedError('Request is not available')

    def get(self, id, side):
        raise NotImplementedError('Request is not available')
