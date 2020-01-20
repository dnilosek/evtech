#!/usr/bin/env python3

"""Tests for ray class."""

import sys
import unittest
import numpy as np
import math

from pyproj import CRS
from evtech import Ray
from evtech import Camera

class TestRay(unittest.TestCase):
    """Tests for `evtech.ray` package."""

    def setUp(self):
        self.proj = np.array([[-234.48497951320869, -11689.146112537686, -3420.9549093694854, 54967162069.77626], 
             [-11527.74509904331, 527.9966478964207, -3108.9307732776556, 2267432568.205459], 
             [0.07731721986909759, 0.01342309733163904, -0.996916676327768, -93150.24955090503]
             ])
        self.bounds = [4405, 655, 5587, 1420]
        self.cen = [411228.51669897616, 4693677.177776167, 1653.5802147550032]
        self.geo_bounds = [-88.07607063663191, 42.387928513288855, -88.07499236028416, 42.38917669615173]
        self.elev = 250.522
        self.crs = CRS.from_user_input(32616)
        self.path = "foo.jpg"
        self.cam = Camera(self.proj, self.bounds, self.cen, self.geo_bounds, self.elev, self.crs, self.path)
        pass


    def test_construct(self):
        ray = Ray([0,0,0],[1,1,1], None)
        
        # Direction should be normalized
        self.assertEqual(ray.origin[0],0)
        self.assertEqual(ray.origin[1],0)
        self.assertEqual(ray.origin[2],0)

        self.assertEqual(ray.direction[0],1.0/math.sqrt(3))
        self.assertEqual(ray.direction[1],1.0/math.sqrt(3))
        self.assertEqual(ray.direction[2],1.0/math.sqrt(3))

    def test_elevation_intersect(self):
        ray = self.cam.project_from_camera(880,443)
        pt = ray.intersect_at_elevation(self.elev)
        self.assertAlmostEqual(pt[2], self.elev)
