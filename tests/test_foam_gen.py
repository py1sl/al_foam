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


class TestCheckOverlap(unittest.TestCase):
    """Test cases for the check_overlap function"""
    
    def test_check_overlap_no_overlap(self):
        """Test two pores that don't overlap"""
        # Pores at (0,0,0) with r=1 and (10,0,0) with r=1
        result = foam_gen.check_overlap(0, 0, 0, 1, 10, 0, 0, 1)
        self.assertFalse(result)
    
    def test_check_overlap_touching(self):
        """Test two pores that are exactly touching"""
        # Pores at (0,0,0) with r=1 and (2,0,0) with r=1
        result = foam_gen.check_overlap(0, 0, 0, 1, 2, 0, 0, 1)
        self.assertFalse(result)
    
    def test_check_overlap_overlapping(self):
        """Test two pores that overlap"""
        # Pores at (0,0,0) with r=1 and (1,0,0) with r=1
        result = foam_gen.check_overlap(0, 0, 0, 1, 1, 0, 0, 1)
        self.assertTrue(result)
    
    def test_check_overlap_same_position(self):
        """Test two pores at the same position"""
        result = foam_gen.check_overlap(5, 5, 5, 1, 5, 5, 5, 1)
        self.assertTrue(result)
    
    def test_check_overlap_3d(self):
        """Test overlap in 3D space"""
        # Pores at (0,0,0) with r=1 and (1,1,1) with r=1
        result = foam_gen.check_overlap(0, 0, 0, 1, 1, 1, 1, 1)
        self.assertTrue(result)


class TestGenerateRandomPores(unittest.TestCase):
    """Test cases for the generate_random_pores function"""
    
    def test_generate_single_pore(self):
        """Test generation of a single pore"""
        pores = foam_gen.generate_random_pores(1, (0, 10), (0, 10), (0, 10), 0.5, 1.0, seed=42)
        self.assertIsNotNone(pores)
        self.assertEqual(len(pores), 1)
        x, y, z, r = pores[0]
        self.assertTrue(0 <= x <= 10)
        self.assertTrue(0 <= y <= 10)
        self.assertTrue(0 <= z <= 10)
        self.assertTrue(0.5 <= r <= 1.0)
    
    def test_generate_multiple_pores(self):
        """Test generation of multiple pores"""
        pores = foam_gen.generate_random_pores(5, (0, 100), (0, 100), (0, 100), 0.5, 2.0, seed=42)
        self.assertIsNotNone(pores)
        self.assertEqual(len(pores), 5)
    
    def test_generate_pores_no_overlap(self):
        """Test that generated pores don't overlap"""
        pores = foam_gen.generate_random_pores(10, (0, 100), (0, 100), (0, 100), 0.5, 2.0, seed=42)
        self.assertIsNotNone(pores)
        # Check all pairs of pores
        for i in range(len(pores)):
            for j in range(i + 1, len(pores)):
                x1, y1, z1, r1 = pores[i]
                x2, y2, z2, r2 = pores[j]
                self.assertFalse(foam_gen.check_overlap(x1, y1, z1, r1, x2, y2, z2, r2),
                               f"Pores {i} and {j} overlap")
    
    def test_generate_pores_impossible(self):
        """Test case where it's impossible to place all pores"""
        # Try to place 100 large pores in a small space
        pores = foam_gen.generate_random_pores(100, (0, 10), (0, 10), (0, 10), 4, 5, max_attempts=10, seed=42)
        self.assertIsNone(pores)
    
    def test_generate_pores_reproducible(self):
        """Test that using the same seed produces the same results"""
        pores1 = foam_gen.generate_random_pores(3, (0, 10), (0, 10), (0, 10), 0.5, 1.0, seed=123)
        pores2 = foam_gen.generate_random_pores(3, (0, 10), (0, 10), (0, 10), 0.5, 1.0, seed=123)
        self.assertEqual(pores1, pores2)
    
    def test_generate_pores_zero_pores(self):
        """Test generation of zero pores"""
        pores = foam_gen.generate_random_pores(0, (0, 10), (0, 10), (0, 10), 0.5, 1.0, seed=42)
        self.assertIsNotNone(pores)
        self.assertEqual(len(pores), 0)


class TestMakePoreSurfLines(unittest.TestCase):
    """Test cases for the make_pore_surf_lines function"""
    
    def test_make_pore_surf_lines_single(self):
        """Test surf line generation for a single pore"""
        pores = [(1.0, 2.0, 3.0, 0.5)]
        surf_lines = foam_gen.make_pore_surf_lines(pores)
        self.assertEqual(len(surf_lines), 1)
        self.assertEqual(surf_lines[0], "1 s 1.0 2.0 3.0 0.5")
    
    def test_make_pore_surf_lines_multiple(self):
        """Test surf line generation for multiple pores"""
        pores = [(1.0, 2.0, 3.0, 0.5), (4.0, 5.0, 6.0, 1.0), (7.0, 8.0, 9.0, 1.5)]
        surf_lines = foam_gen.make_pore_surf_lines(pores)
        self.assertEqual(len(surf_lines), 3)
        self.assertEqual(surf_lines[0], "1 s 1.0 2.0 3.0 0.5")
        self.assertEqual(surf_lines[1], "2 s 4.0 5.0 6.0 1.0")
        self.assertEqual(surf_lines[2], "3 s 7.0 8.0 9.0 1.5")
    
    def test_make_pore_surf_lines_empty(self):
        """Test surf line generation for empty list"""
        pores = []
        surf_lines = foam_gen.make_pore_surf_lines(pores)
        self.assertEqual(len(surf_lines), 0)
    
    def test_make_pore_surf_lines_numbering(self):
        """Test that surf lines are numbered correctly"""
        pores = [(0, 0, 0, 1), (10, 10, 10, 2), (20, 20, 20, 3)]
        surf_lines = foam_gen.make_pore_surf_lines(pores)
        # Check that numbering starts at 1 and increments
        for i, line in enumerate(surf_lines, start=1):
            parts = line.split()
            self.assertEqual(int(parts[0]), i)


if __name__ == '__main__':
    unittest.main()
