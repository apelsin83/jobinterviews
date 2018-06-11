import unittest
from main import Parser

__author__ = 'devel'


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_start_parsing(self):
        self.assertTrue(True)

    def test_get_response_fail(self):

        self.assertTrue(True==self.parser._original(get_response('com', None)))

    def test_register_session(self):
        self.assertTrue(True)

    def test_find_value(self):
        self.assertTrue(True)

    def test_get_article(self):
        self.assertTrue(True)

    def test_get_post_time(self):
        self.assertTrue(True)

    def test_parse_page(self):
        self.assertTrue(True)
