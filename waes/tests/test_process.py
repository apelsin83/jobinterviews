import unittest as ut
from mock import Mock
from bl.processing import check_request, save_file


class TestCheckRequest(ut.TestCase):

    def setUp(self):
        self.request = Mock()

    def test_check_request_without_necessary_headers(self):
        self.request.headers = {'Content-Type': "application/json2"}
        ok, data = check_request(self.request, 5)
        self.assertFalse(ok)
        self.assertDictEqual(
            data, {'error': 'Request should contains header: Content-Type: application/json'})

    def test_check_request_without_necessary_json_fields(self):
        self.request.headers = {'Content-Type': "application/json"}
        self.request.json = {'payload2': "fsdf"}
        ok, data = check_request(self.request, 5)
        self.assertFalse(ok)
        self.assertDictEqual(
            data, {'error': 'Wrong json structure: {payload: xxx}'})

    def test_check_request(self):
        self.request.headers = {'Content-Type': "application/json"}
        self.request.json = {'payload': "fsdf"}
        ok, data = check_request(self.request, 5)
        self.assertTrue(ok)
        self.assertEqual(data, "fsdf")

    def test_check_request_wrong_ip(self):
        self.request.headers = {'Content-Type': "application/json"}
        self.request.json = {'payload': "fsdf"}
        ok, data = check_request(self.request, 'd2222')
        self.assertFalse(ok)
        self.assertDictEqual(
            data, {'error': 'Id should be a integer'})


class TestCompareFiles(ut.TestCase):

    def setUp(self):
        self.data_layer = Mock()

    def test_save_file_without_error(self):
        self.data_layer.save = Mock()
        save_file(5, 'left', 'df', self.data_layer)
        self.data_layer.save.assert_called_once_with(5, 'left', 'df')
