import unittest

from everything import *


class TestTimeUnits(unittest.TestCase):

    def test_matched_units_return_True(self):
        f = Flow(tunit="Leapyear")
        s = Simulator([f], tunit="Leapyear")
        self.assertTrue(s.check_time_units())

    def test_mismatched_units_raise_UnitsError(self):
        f = Flow(tunit="centuries")
        s = Simulator([f])
        self.assertRaises(UnitsError, s.check_time_units)

    def test_default_units_is_second(self):
        f = Flow(tunit="Second")
        s = Simulator([f])
        self.assertTrue(s.check_time_units())


if __name__ == '__main__':
    unittest.main()
