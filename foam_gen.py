import numpy as np

def make_cube(x,y,z, side_length):
    """ """
    volume = side_length * side_length * side_length
    corners = [(x,y,z), (x+side_length,y,z), (x, y+side_length, z), (x,y,z+side_length), 
              (x+side_length, y+side_length, z), (x+side_length, y+side_length, z+side_length), 
              (x+side_length, y, z+side_length), (x, y+side_length, z+side_length)]
    
    return volume

def make_spherical_pore(x, y, z, rad, num=1):
    """ """
    surf_str = str(num) + " s " + str(x) + " " + str(y) + " " + str(z) + " " + str(rad)
    return surf_str

def check_overlap(x1, y1, z1, r1, x2, y2, z2, r2):
    """
    Check if two spherical pores overlap.
    
    Args:
        x1, y1, z1: Position of first pore center
        r1: Radius of first pore
        x2, y2, z2: Position of second pore center
        r2: Radius of second pore
    
    Returns:
        bool: True if pores overlap, False otherwise
    """
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    return distance < (r1 + r2)

def generate_random_pores(num_pores, x_range, y_range, z_range, r_min, r_max, max_attempts=1000, seed=None):
    """
    Generate x number of non-overlapping spherical pores with random positions and radii.
    
    Args:
        num_pores: Number of pores to generate
        x_range: Tuple (min, max) for x coordinates
        y_range: Tuple (min, max) for y coordinates
        z_range: Tuple (min, max) for z coordinates
        r_min: Minimum radius
        r_max: Maximum radius
        max_attempts: Maximum attempts to place each pore before giving up
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

def make_pore_surf_lines(pores):
    """
    Create a list of surf lines for a list of pores.
    
    Args:
        pores: List of tuples (x, y, z, radius) for each pore
    
    Returns:
        list: List of surf line strings
    """
    surf_lines = []
    for i, (x, y, z, r) in enumerate(pores, start=1):
        surf_line = make_spherical_pore(x, y, z, r, num=i)
        surf_lines.append(surf_line)
    
    return surf_lines
