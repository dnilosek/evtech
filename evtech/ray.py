"""Ray class for evtech."""

import numpy as np
from sklearn import preprocessing

class Ray():
    """ A class to represent rays in three dimensional space
    
    :param origin: A 3 elemnt list representing the origin of the ray
    :type origin: class: list
    :param direction: A 3 element list representing the direction of the ray
    :type direction: list
    :param crs: The CRS for the coordinates of the ray
    :type crs: class: `pyproj.CRS`
    """

    def __init__(self, origin, direction, crs):
        """ Constructor method
        """
        self.origin = np.transpose(np.array([origin]))
        self.direction = np.transpose(preprocessing.normalize(np.array([direction]), norm='l2'))
        self.crs = crs