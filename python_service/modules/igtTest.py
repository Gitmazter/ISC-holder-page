import unittest
import time
from python_service.modules.igt_calc_helpers import calculate_igt_points

test_wtarr1 = [{ 'timeStamp': 0, 'weight': 1, 'supply': 1},{ 'timeStamp': 5, 'weight': 1, 'supply': 2} ]
test_txs1 = [{'timeStamp': 0, 'newBalance':1}]

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual(calculate_igt_points(test_txs1, test_wtarr1), time.time()/86400)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

if __name__ == '__main__':
    unittest.main()