
import unittest
import numpy as np
from angle_calculator import calculate_angle

class TestAngleCalculations(unittest.TestCase):

    def test_calculate_angle(self):
        """Test the core angle calculation function with known points."""
        # Test for a 90-degree angle
        p1 = (0, 0)
        p2 = (0, 1)
        p3 = (1, 1)
        self.assertAlmostEqual(calculate_angle(p1, p2, p3), 90.0, places=1)

        # Test for a 180-degree angle (straight line)
        p1 = (0, 0)
        p2 = (1, 0)
        p3 = (2, 0)
        self.assertAlmostEqual(calculate_angle(p1, p2, p3), 180.0, places=1)

        # Test for a 45-degree angle
        p1 = (1, 0)
        p2 = (0, 0)
        p3 = (1, 1)
        self.assertAlmostEqual(calculate_angle(p1, p2, p3), 45.0, places=1)

if __name__ == '__main__':
    unittest.main()
