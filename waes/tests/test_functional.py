import unittest
import shutil
import json
from webtest import TestApp
from main import application
from settings import FILE_DB_SETTINGS


class SaveFileTests(unittest.TestCase):

    def setUp(self):
        self.testapp = TestApp(application)

    def tearDown(self):
        try:
            shutil.rmtree(FILE_DB_SETTINGS['folder'])
        except:
            pass

    def test_not_allowed_uri(self):
        res = self.testapp.get('/', status=403)
        self.assertEqual(403, res.status_code)
        self.assertEqual('403 Forbidden', res.status)
        self.assertEqual('', res.body)

    def test_post_with_wrong_headers(self):
        res = self.testapp.post_json(
            '/v1/diff/1/left', {'payload': ''},
            headers={'Content-Type': 'application/json1'}, status=400)
        self.assertEqual(400, res.status_code)
        self.assertEqual('400 Bad Request', res.status)
        self.assertEqual(
            '{"error": "Request should contains header: Content-Type: application/json"}', res.body)

    def test_post_with_wrong_json(self):
        res = self.testapp.post_json(
            '/v1/diff/1/left', {'fggf': ''},
            headers={'Content-Type': 'application/json'}, status=400)
        self.assertEqual(400, res.status_code)
        self.assertEqual('400 Bad Request', res.status)
        self.assertEqual(
            '{"error": "Wrong json structure: {payload: xxx}"}', res.body)

    def test_post_with_fixed_left_json(self):
        res = self.testapp.post_json(
            '/v1/diff/1/left', {'payload': 'sds21'},
            headers={'Content-Type': 'application/json'}, status=200)
        self.assertEqual(200, res.status_code)
        self.assertEqual('200 OK', res.status)
        self.assertEqual('', res.body)

    def test_post_with_fixed_right_json(self):
        res = self.testapp.post_json(
            '/v1/diff/1/right', {'payload': 'sds21'},
            headers={'Content-Type': 'application/json'}, status=200)
        self.assertEqual(200, res.status_code)
        self.assertEqual('200 OK', res.status)
        self.assertEqual('', res.body)


class DiffFileTests(unittest.TestCase):

    def setUp(self):
        self.testapp = TestApp(application)

    def tearDown(self):
        try:
            shutil.rmtree(FILE_DB_SETTINGS['folder'])
        except:
            pass

    def test_diff_without_data(self):
        res = self.testapp.get('/v1/diff/1', status=400)
        self.assertEqual(400, res.status_code)
        self.assertEqual('400 Bad Request', res.status)
        self.assertEqual('{"error": "File with id = 1 and side = left is not provided"}',
                         res.body)

    def test_diff_without_right_data(self):
        self.testapp.post_json('/v1/diff/1/left', {'payload': 'sds21'},
                               headers={'Content-Type': 'application/json'}, status=200)
        res = self.testapp.get('/v1/diff/1', status=400)
        self.assertEqual(400, res.status_code)
        self.assertEqual('400 Bad Request', res.status)
        self.assertEqual('{"error": "File with id = 1 and side = right is not provided"}',
                         res.body)

    def test_diff_without_left_data(self):
        self.testapp.post_json('/v1/diff/1/right', {'payload': 'sds21'},
                               headers={'Content-Type': 'application/json'}, status=200)
        res = self.testapp.get('/v1/diff/1', status=400)
        self.assertEqual(400, res.status_code)
        self.assertEqual('400 Bad Request', res.status)
        self.assertEqual('{"error": "File with id = 1 and side = left is not provided"}',
                         res.body)

    def test_diff_with_diffrent_length_data(self):
        self.testapp.post_json('/v1/diff/1/left', {'payload': 'sds21d'},
                               headers={'Content-Type': 'application/json'}, status=200)
        self.testapp.post_json('/v1/diff/1/right', {'payload': 'sds21'},
                               headers={'Content-Type': 'application/json'}, status=200)
        res = self.testapp.get('/v1/diff/1', status=200)
        self.assertEqual(200, res.status_code)
        self.assertEqual('200 OK', res.status)
        self.assertEqual('{"payload": "Different length"}',
                         res.body)

    def test_diff_with_equal_data(self):
        self.testapp.post_json('/v1/diff/1/left', {'payload': 'sds21'},
                               headers={'Content-Type': 'application/json'}, status=200)
        self.testapp.post_json('/v1/diff/1/right', {'payload': 'sds21'},
                               headers={'Content-Type': 'application/json'}, status=200)
        res = self.testapp.get('/v1/diff/1', status=200)
        self.assertEqual(200, res.status_code)
        self.assertEqual('200 OK', res.status)
        self.assertEqual('{"payload": "Equal"}',
                         res.body)

    def test_diff_with_equal_length_diff_data(self):
        self.testapp.post_json('/v1/diff/1/left', {'payload': 'sas21'},
                               headers={'Content-Type': 'application/json'}, status=200)
        self.testapp.post_json('/v1/diff/1/right', {'payload': 'sds21'},
                               headers={'Content-Type': 'application/json'}, status=200)
        res = self.testapp.get('/v1/diff/1', status=200)
        self.assertEqual(200, res.status_code)
        self.assertEqual('200 OK', res.status)
        self.assertDictEqual({"payload": [{"length": 1, "offset": 1}]},
                         json.loads(res.body))