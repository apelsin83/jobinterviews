import os
import errno
import shutil
import time
import gevent
from base_db import BaseDbInterface
from cleaner import clear_loop


class FileDb(BaseDbInterface):

    def __init__(self, folder='db'):
        # Init all staff for starage
        self.folder = folder
        self._init_object()

    def _init_object(self):
        # create storage folder
        try:
            os.makedirs(self.folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        # Run cleaner thread
        gevent.spawn(clear_loop, self.folder)

    def _get_path(self, id, side):
        return os.path.join(self.folder, '%s_%s' % (id, side))

    def get(self, id, side):
        path = self._get_path(id, side)
        data = None
        # locking file and read data from it 
        with LockDir(path):
            with open(path, 'rb') as df:
                data = df.read()
        return data

    def save(self, id, side, data):
        path = self._get_path(id, side)
        # locking file and save data to it 
        with LockDir(path):
            with open(path, 'wb') as df:
                df.write(data)


class LockDir(object):

    def __init__(self, path):
        self.dir_path = '%s.lock' % path
        try:
            os.makedirs(self.dir_path)
            lock_file = os.path.join(self.dir_path, 'lock')
            with open(lock_file, 'wb') as df:
                df.write(str(time.time()))
        except OSError as e:
            if e.errno == errno.EEXIST:
                raise OSError("Can't use file %s." % path)

    def __enter__(self):
        return

    def __exit__(self, *args):
        try:
            shutil.rmtree(self.dir_path)
        except OSError:
            pass
        
