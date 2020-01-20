#!/usr/bin/env python3

"""Tests for camera class."""

import sys
import unittest
import numpy as np 

from pyproj import CRS
from evtech import Camera
from evtech import camera_from_json

class TestCamera(unittest.TestCase):
    """Tests for `evtech.camera` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.proj = np.array([
		    [-11920.719528081565, -1.54881175469775, -2717.588268249619, 5850678375.023631],
		    [-21.77201952354797, 11688.504705879252, -2613.2282740925775, -51415498526.18434],
		    [-0.05013907005013629, -0.03348284191759311, -0.9981808350981529, 174400.24754747818]
	    ])
        self.bounds = [3294, 949, 3656, 1195]
        self.cen = [489652.8811968585, 4400284.38696494, 2520.0653300965037, 1.0]
        self.geo_bounds = [-105.12153711031904, 39.75137947368138, -105.1212480998424, 39.751532181111685]
        self.elev = 1717.2020042918448
        self.crs = CRS.from_user_input(32613)
        self.path = "foo.jpg"
        self.cam = Camera(self.proj, self.bounds, self.cen, self.geo_bounds, self.elev, self.crs, self.path)
        pass
    
    def test_set_imagepath(self):
        newpath = "bar.jpg"
        self.cam.set_path(newpath)
        self.assertEqual(newpath, self.cam.image_path)

    def test_project_to_camera(self):
        # Top left corner from geo bounds, should be within the 0,0 pixel
        pt = self.cam.project_to_camera(self.geo_bounds[2], self.geo_bounds[1], self.elev)
        self.assertTrue(pt[0] >= 0 and pt[0] < 1)
        self.assertTrue(pt[1] >= 0 and pt[1] < 1)

        # Bottom right should fall in last pixel idex
        x_idx = self.bounds[2] - self.bounds[0]
        y_idx = self.bounds[3] - self.bounds[1]
        pt = self.cam.project_to_camera(self.geo_bounds[0], self.geo_bounds[3], self.elev)
        self.assertTrue(pt[0] >= x_idx and pt[0] < x_idx+1)
        self.assertTrue(pt[1] >= y_idx and pt[1] < y_idx+1)

    def test_project_from_camera(self):
        ray = self.cam.project_from_camera(0,0)
        self.assertEqual(ray.origin[0], self.cen[0])
        self.assertEqual(ray.origin[1], self.cen[1])
        self.assertEqual(ray.origin[2], self.cen[2])

    def test_to_full_image(self):
        x, y = self.cam.to_full_image(0,0)
        self.assertEqual(x, self.bounds[0])
        self.assertEqual(y, self.bounds[1])

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
        # Ensure conversion done correctly
        self.assertEqual(str(cam.crs),"epsg:32613")

    def test_loadimage(self):

        def loader(img):
            return self.path == img
        self.assertTrue(self.cam.load_image(loader))

    def test_hightbetweenpoints(self):
        cam1_json = {
            "id": "13470217", 
            "shot_id": "13470217_E_ILZLAK020024NeighObliq7313E_150610.jpg", 
            "warehouse_id": 26946, 
            "projection": [[1525.5867281279347, -15512.91424561646, -2311.8378111550846, 72183965325.08594], 
            [-7573.84425712711, 803.6272922226443, -13570.519962708786, -650749980.3668021], 
            [0.7925646349229568, -0.045523902505363464, -0.608173942069206, -109441.04682805175]], 
            "bounds": [125, 267, 966, 550], 
            "camera_center": [408968.8416940464, 4693116.473847266, 1716.97110001749], 
            "geo_bounds": [-88.07612165733431, 42.38789365082783, -88.07494134030249, 42.389211554600976], 
            "elevation": 254.16879272460938, 
            "orientation": "E"
        }
        cam1 = camera_from_json(cam1_json)
        base_pt = [41,118]
        peak_pt = [35,90]

        height = cam1.height_between_points(base_pt, peak_pt)
        self.assertAlmostEqual(height, 5.51879092088098)

        height = cam1.height_between_points(base_pt, peak_pt, cam1.elevation)
        self.assertAlmostEqual(height, 5.51879092088098)