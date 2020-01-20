"""Ray class for evtech."""

import numpy as np
from sklearn import preprocessing
from pyproj import CRS, Transformer

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

    def point_at_depth(self, depth):
        """ Return a 3D point at a given depth along the ray
        
        :param depth: The depth along the ray
        :type depth: float
        :return: A 3d point
        :rtype: numpy.array
        """
        return self.origin + depth * self.direction

    def depth_at_elevation(self, elevation):
        """ Return the depth at a given elevation
        
        :param elevation: The elevation to get the depth of
        :type elevation: float
        """
        return (elevation - self.origin[2])/self.direction[2]

    def intersect_at_elevation(self, elevation, latlng=True):
        """Return a three dimensional point intersected at a given elevation
        
        :param elevation: The elevation to intersect
        :type elevation: float
        :param latlng: Return the point as lat,lng, elevation, defaults to True
        :type latlng: bool, optional
        :return: A 3d point
        :rtype: numpy.array
        """
        
        depth = self.depth_at_elevation(elevation)
        pt = self.point_at_depth(depth)

        if latlng:
            transformer = Transformer.from_crs(self.crs, CRS.from_user_input(4326), always_xy=True)
            pt[0],pt[1],pt[2] = transformer.transform(pt[0], pt[1], pt[2])
    
        [pt] = np.transpose(pt)
        return pt