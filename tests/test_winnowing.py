"""Unit tests for the winnowing c extention. If the c extention failed
to build, the tests will fail with a ModuleNotFoundError.
"""

from copydetect.winnow import _winnow
import numpy as np
import unittest

class WinnowOutputTestCase(unittest.TestCase):
    """Ensure that winnowing generates the correct output for several
    selections of window_size using an example list. Also checks the
    behavior of winnowing for an empty input list and a window size
    larger than the input list
    """
    def setUp(self):
        test_list = [-15, -6, -8, 9, 6, -2, -2, 0, -16, -12,
                      2, -12, -14, 18, -14, 18, 0, 5, 3, -19]
        self.test_arr = np.array(test_list)

    def test_winnow_empty(self):
        winnow_empty = np.array([])
        out_empty = _winnow(np.array([]), 3)
        self.assertTrue(np.array_equal(out_empty, winnow_empty))

    def test_winnow_1(self):
        winnow_1 = np.array(np.arange(20))
        out_1 = _winnow(self.test_arr, 1)
        self.assertTrue(np.array_equal(out_1, winnow_1))

    def test_winnow_2(self):
        winnow_2 = np.array([0, 2, 4, 5, 6, 8, 9, 11, 12, 14, 16, 18, 19])
        out_2 = _winnow(self.test_arr, 2)
        self.assertTrue(np.array_equal(out_2, winnow_2))

    def test_winnow_3(self):
        winnow_3 = np.array([0, 2, 5, 8, 11, 12, 14, 16, 19])
        out_3 = _winnow(self.test_arr, 3)
        self.assertTrue(np.array_equal(out_3, winnow_3))

    def test_winnow_inf(self):
        winnow_25 = np.array([0, 8, 19])
        out_25 = _winnow(self.test_arr, 25)
        self.assertTrue(np.array_equal(out_25, winnow_25))

class WinnowDensityTestCase(unittest.TestCase):
    """Ensure that the output density from several random winnowing
    runs falls within a sane range. The bounds are VERY generous.
    """
    def test_winnow_density(self):
        in_range = True
        for win_size in range(2, 20):
            expected_density = 2/(win_size + 1)*10000
            rand_hashes = np.random.randint(-9223372036854775808,
                                             9223372036854775807, 10000)
            density = len(_winnow(rand_hashes, win_size))

            if not (density > expected_density - 200 and
                    density < expected_density + 200):
                in_range = False
        self.assertTrue(in_range)

if __name__ == '__main__':
    unittest.main()