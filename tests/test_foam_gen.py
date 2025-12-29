import unittest
import sys
import os

# Add parent directory to path to import foam_gen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import foam_gen


class TestMakeCube(unittest.TestCase):
    """Test cases for the make_cube function"""
    
    def test_make_cube_unit_cube(self):
        """Test volume calculation for a unit cube (1x1x1)"""
        volume = foam_gen.make_cube(0, 0, 0, 1)
        self.assertEqual(volume, 1)
    
    def test_make_cube_2x2x2(self):
        """Test volume calculation for a 2x2x2 cube"""
        volume = foam_gen.make_cube(0, 0, 0, 2)
        self.assertEqual(volume, 8)
    
    def test_make_cube_different_position(self):
        """Test that cube position doesn't affect volume"""
        volume1 = foam_gen.make_cube(0, 0, 0, 3)
        volume2 = foam_gen.make_cube(10, 20, 30, 3)
        self.assertEqual(volume1, volume2)
        self.assertEqual(volume1, 27)
    
    def test_make_cube_decimal_side_length(self):
        """Test volume calculation with decimal side length"""
        volume = foam_gen.make_cube(0, 0, 0, 2.5)
        self.assertAlmostEqual(volume, 15.625)
    
    def test_make_cube_zero_side_length(self):
        """Test volume calculation with zero side length"""
        volume = foam_gen.make_cube(0, 0, 0, 0)
        self.assertEqual(volume, 0)


class TestMakeSphericalPore(unittest.TestCase):
    """Test cases for the make_spherical_pore function"""
    
    def test_make_spherical_pore_default_num(self):
        """Test spherical pore string with default num parameter"""
        result = foam_gen.make_spherical_pore(1.0, 2.0, 3.0, 0.5)
        self.assertEqual(result, "1 s 1.0 2.0 3.0 0.5")
    
    def test_make_spherical_pore_custom_num(self):
        """Test spherical pore string with custom num parameter"""
        result = foam_gen.make_spherical_pore(5, 10, 15, 2.5, num=3)
        self.assertEqual(result, "3 s 5 10 15 2.5")
    
    def test_make_spherical_pore_zero_coordinates(self):
        """Test spherical pore at origin"""
        result = foam_gen.make_spherical_pore(0, 0, 0, 1.0)
        self.assertEqual(result, "1 s 0 0 0 1.0")
    
    def test_make_spherical_pore_negative_coordinates(self):
        """Test spherical pore with negative coordinates"""
        result = foam_gen.make_spherical_pore(-5, -10, -15, 3.0, num=2)
        self.assertEqual(result, "2 s -5 -10 -15 3.0")
    
    def test_make_spherical_pore_string_format(self):
        """Test that the output format matches expected pattern"""
        result = foam_gen.make_spherical_pore(1.5, 2.5, 3.5, 0.75, num=5)
        parts = result.split()
        self.assertEqual(len(parts), 6)
        self.assertEqual(parts[0], "5")
        self.assertEqual(parts[1], "s")


if __name__ == '__main__':
    unittest.main()
