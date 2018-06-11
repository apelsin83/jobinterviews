import unittest as ut
import shutil
import os
import time
from cleaner import clear


class TestCheckRequest(ut.TestCase):

    def setUp(self):
        self.location = 'testdb'
        try:
            os.makedirs(self.location)
        except:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(self.location)
        except:
            pass

    def test_clear_location_no_lock(self):
        clear(self.location, 5)
        self.assertEqual([], os.listdir(self.location))

    def test_clear_location_not_expired_lock(self):
        path_fo = os.path.join(self.location, '1_left.lock')
        lock_file = os.path.join(path_fo, 'lock')
        os.makedirs(path_fo)
        with open(lock_file, 'wb') as df:
            df.write(str(time.time()))
        clear(self.location, 10)
        self.assertEqual(['1_left.lock'], os.listdir(self.location))

    def test_clear_location_with_expired_lock(self):
        path_fo = os.path.join(self.location, '1_left.lock')
        lock_file = os.path.join(path_fo, 'lock')
        os.makedirs(path_fo)
        with open(lock_file, 'wb') as df:
            df.write(str(time.time() - 50))
        clear(self.location, 10)
        self.assertEqual([], os.listdir(self.location))

    def test_clear_location_with_exception(self):
        path_fo = os.path.join(self.location, '1_left.lock')
        lock_file = os.path.join(path_fo, 'lock')
        os.makedirs(path_fo)
        with open(lock_file, 'wb') as df:
            df.write('sfsdf')
        clear(self.location, 10)
        self.assertEqual(['1_left.lock'], os.listdir(self.location))
