import unittest
from everything import *

class TestTimeUnits(unittest.TestCase):
    def test_matched_units_return_True(self):
        f = Flow(time_step="Leapyear")
        s = Simulator([f], time_step="Leapyear")
        self.assertEqual("Units OK", s.reconcile_time_units())
    def test_mismatched_units_raise_UnitsError(self):
        f = Flow(time_step="centuries")
        s = Simulator([f])
        self.assertRaises(UnitsError, s.reconcile_time_units)
    def test_default_units_is_second(self):
        f = Flow(time_step="Second")
        s = Simulator([f])
        self.assertEqual("Units OK", s.reconcile_time_units())


if __name__ == '__main__':
    unittest.main()
