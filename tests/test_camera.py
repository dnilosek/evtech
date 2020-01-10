#!/usr/bin/env python3

"""Tests for camera class."""

import sys
import unittest
import numpy as np 

from pyproj import CRS
from evtech import Camera
from evtech import camera_from_json

class TestCamera(unittest.TestCase):
    """Tests for `evtech` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.proj = np.array([
		    [-11920.719528081565, -1.54881175469775, -2717.588268249619, 5850678375.023631],
		    [-21.77201952354797, 11688.504705879252, -2613.2282740925775, -51415498526.18434],
		    [-0.05013907005013629, -0.03348284191759311, -0.9981808350981529, 174400.24754747818]
	    ])
        self.bounds = [3294, 949, 3656, 1195]
        self.cen = [489652.8811968585, 4400284.38696494, 2520.0653300965037]
        self.geo_bounds = [-105.12153711031904, 39.75137947368138, -105.1212480998424, 39.751532181111685]
        self.elev = 1717.2020042918448
        self.crs = CRS.from_user_input(32613)
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_construct(self):
        """Test something."""
        cam = Camera(self.proj, self.bounds, self.cen, self.geo_bounds, self.elev, self.crs)

    def test_fromjson(self):
        data = {
            "id": "18274434", 
            "warehouse_id": "40604", 
            "projection": [[-11920.719528081565, -1.54881175469775, -2717.588268249619, 5850678375.023631], 
            [-21.77201952354797, 11688.504705879252, -2613.2282740925775, -51415498526.18434], 
            [-0.05013907005013629, -0.03348284191759311, -0.9981808350981529, 174400.24754747818]], 
            "bounds": [3294, 949, 3656, 1195], 
            "camera_center": [489652.8811968585, 4400284.38696494, 2520.0653300965037], 
            "geo_bounds": [-105.12153711031904, 39.75137947368138, -105.1212480998424, 39.751532181111685], 
            "elevation": 1717.2020042918448
        }

        cam = camera_from_json(data)
        self.assertEqual(str(cam.crs),"epsg:32613")