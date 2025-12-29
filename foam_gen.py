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
  
