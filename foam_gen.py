"""
Aluminum Foam Generator Module

This module provides functions to generate aluminum foam models with spherical pores
for use in Monte Carlo N-Particle (MCNP) simulations. It includes utilities for:
- Generating random non-overlapping spherical pores
- Creating MCNP surface definitions
- Building MCNP cell definitions
- Checking geometric overlaps

The foam models are useful for simulating solid methane moderators with
realistic aluminum foam structures.
"""
from typing import Optional
import numpy as np

def make_cube(x: float, y: float, z: float, side_length: float) -> float:
    """
    Calculate the volume of a cube at the specified position.
    
    Args:
        x: X-coordinate of the cube origin
        y: Y-coordinate of the cube origin
        z: Z-coordinate of the cube origin
        side_length: Length of each side of the cube
        
    Returns:
        float: Volume of the cube (side_length^3)
    """
    volume = side_length * side_length * side_length
    corners = [(x, y, z), (x+side_length, y, z), (x, y+side_length, z), (x, y, z+side_length), 
              (x+side_length, y+side_length, z), (x+side_length, y+side_length, z+side_length), 
              (x+side_length, y, z+side_length), (x, y+side_length, z+side_length)]
    
    return volume

def make_spherical_pore_string(x: float, y: float, z: float, rad: float, num: int = 1) -> str:
    """
    Generate an MCNP surface string for a spherical pore.
    
    Args:
        x: X-coordinate of the sphere center
        y: Y-coordinate of the sphere center
        z: Z-coordinate of the sphere center
        rad: Radius of the sphere
        num: Surface number identifier (default: 1)
        
    Returns:
        str: MCNP-formatted surface string (e.g., "1 s 0 0 0 1.5")
    """
    surf_str = f"{num} s {x} {y} {z} {rad}"
    return surf_str


# Backward compatibility alias
make_spherical_pore = make_spherical_pore_string

def check_overlap(x1: float, y1: float, z1: float, r1: float, 
                  x2: float, y2: float, z2: float, r2: float) -> bool:
    """
    Check if two spherical pores overlap.
    
    Args:
        x1: X-coordinate of first pore center
        y1: Y-coordinate of first pore center
        z1: Z-coordinate of first pore center
        r1: Radius of first pore
        x2: X-coordinate of second pore center
        y2: Y-coordinate of second pore center
        z2: Z-coordinate of second pore center
        r2: Radius of second pore
        
    Returns:
        bool: True if pores overlap, False otherwise
    """
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return distance < (r1 + r2)

def generate_random_pores(num_pores: int, x_range: tuple[float, float], 
                         y_range: tuple[float, float], z_range: tuple[float, float], 
                         r_min: float, r_max: float, max_attempts: int = 1000, 
                         seed: Optional[int] = None) -> Optional[list[tuple[float, float, float, float]]]:
    """
    Generate a specified number of non-overlapping spherical pores with random positions and radii.
    
    Args:
        num_pores: Number of pores to generate
        x_range: Tuple (min, max) for x coordinates
        y_range: Tuple (min, max) for y coordinates
        z_range: Tuple (min, max) for z coordinates
        r_min: Minimum radius
        r_max: Maximum radius
        max_attempts: Maximum attempts to place each pore before giving up (default: 1000)
        seed: Random seed for reproducibility (optional)
        
    Returns:
        list: List of tuples (x, y, z, radius) for each pore, or None if unable to place all pores
    """
    if seed is not None:
        np.random.seed(seed)
    
    pores = []
    
    for i in range(num_pores):
        placed = False
        for attempt in range(max_attempts):
            # Generate random position and radius
            x = np.random.uniform(x_range[0], x_range[1])
            y = np.random.uniform(y_range[0], y_range[1])
            z = np.random.uniform(z_range[0], z_range[1])
            r = np.random.uniform(r_min, r_max)
            
            # Check if this pore overlaps with any existing pores
            overlaps = False
            for existing_x, existing_y, existing_z, existing_r in pores:
                if check_overlap(x, y, z, r, existing_x, existing_y, existing_z, existing_r):
                    overlaps = True
                    break
            
            if not overlaps:
                pores.append((x, y, z, r))
                placed = True
                break
        
        if not placed:
            # Unable to place pore after max_attempts
            return None
    
    return pores

def make_pore_surf_lines(pores: list[tuple[float, float, float, float]]) -> list[str]:
    """
    Create a list of surf lines for a list of pores.
    
    Args:
        pores: List of tuples (x, y, z, radius) for each pore
        
    Returns:
        list: List of MCNP surf line strings
    """
    surf_lines = []
    for i, (x, y, z, r) in enumerate(pores, start=1):
        surf_line = make_spherical_pore_string(x, y, z, r, num=i)
        surf_lines.append(surf_line)
    
    return surf_lines



def output_mcnp(lines: list[str], fname: str = "t1.i") -> list[str]:
    """
    Output MCNP input deck to file.
    
    Args:
        lines: List of MCNP input lines to write
        fname: Output filename (default: "t1.i")
        
    Returns:
        list: The input lines (for testing/validation purposes)
        
    Note:
        Currently, this function only returns the lines without writing to file.
        File writing functionality should be implemented when needed.
    """
    return lines


def make_mcnp_solid_cell(box: tuple, surf_list: list, cell_num: int = 1, 
                        mat_num: int = 1, dens: float = 2.7) -> str:
    """
    Create an MCNP cell definition string for a solid cell.
    
    Args:
        box: Bounding box definition (currently unused, placeholder for future implementation)
        surf_list: List of surface numbers defining the cell geometry
        cell_num: Cell number identifier (default: 1)
        mat_num: Material number (default: 1)
        dens: Material density in g/cm³ (default: 2.7 for aluminum)
        
    Returns:
        str: MCNP-formatted cell definition string
        
    Note:
        This is a simplified implementation. Full MCNP cell definitions require
        geometry specifications using surface numbers from surf_list.
    """
    cell_str = f"{cell_num} {mat_num} {dens}"
    return cell_str


def main() -> None:
    """
    Main function to generate aluminum foam model with random spherical pores.
    
    Generates 40 random non-overlapping pores within a 10x10x10 cube with
    radii between 0.001 and 0.1, creates MCNP surface definitions, and
    prepares output lines for MCNP input deck.
    """
    lines = []
    pores = generate_random_pores(40, (0, 10), (0, 10), (0, 10), 0.001, 0.1)
    
    if pores is None:
        print("Warning: Unable to place all requested pores. Try reducing the number of pores or increasing the volume.")
        return
    
    surf_lines = make_pore_surf_lines(pores)
    cell_str = make_mcnp_solid_cell(box=None, surf_list=[])
    lines.append(cell_str)
    lines.append("")

    for line in surf_lines:
        lines.append(line)

    lines.append("")
    lines.append("")
    
    output_mcnp(lines)
