import unittest as ut
from mock import Mock
from bl.comparison import compare, compare_files


class TestCompare(ut.TestCase):

    def test_compare_different_length(self):
        result = compare('as', 'gas')
        self.assertDictEqual(result, {'payload': 'Different length'})

    def test_compare_equal(self):
        result = compare('as', 'as')
        self.assertDictEqual(result, {'payload': 'Equal'})

    def test_compare_empty_strings(self):
        result = compare('', '')
        self.assertDictEqual(result, {'payload': 'Equal'})

    def test_compare_diff_strings_one_symbol(self):
        # first
        result = compare('212345', '012345')
        self.assertDictEqual(result, {'payload': [{'length': 1, 'offset': 0}]})
        # middle
        result = compare('012245', '012345')
        self.assertDictEqual(result, {'payload': [{'length': 1, 'offset': 3}]})
        # end
        result = compare('012346', '012345')
        self.assertDictEqual(result, {'payload': [{'length': 1, 'offset': 5}]})

    def test_compare_diff_strings_multi_symbol(self):
        result = compare('212665', '012345')
        self.assertDictEqual(
            result, {'payload': [{'length': 1, 'offset': 0}, {'length': 2, 'offset': 3}]})
        result = compare('asd3k677', '01234688')
        self.assertDictEqual(result, {'payload': [{'length': 3, 'offset': 0}, {
                             'length': 1, 'offset': 4}, {'length': 2, 'offset': 6}]})


class TestCompareFiles(ut.TestCase):

    def setUp(self):
        self.data_layer = Mock()

    def test_compare_files(self):
        self.data_layer.get = Mock(return_value='wheeeeee')
        result = compare_files(5, self.data_layer)
        self.assertDictEqual(result, {'payload': 'Equal'})

    def test_compare_files_not_exists(self):
        msg = 'File with id = 5 and side = left is not provided'
        self.data_layer.get = Mock(side_effect=IOError(msg))
        with self.assertRaises(IOError) as context:
            compare_files(5, self.data_layer)
        self.assertTrue(msg in context.exception)

