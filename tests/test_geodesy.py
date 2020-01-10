#!/usr/bin/env python3

"""Tests for geodesy functions."""

import unittest

from evtech import utm_crs_from_latlon

class TestGeodesy(unittest.TestCase):
    """Tests for `evtech.geodesy` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.lon = -105.12153711031904
        self.lat = 39.75137947368138
        pass

    def test_utm_crs_from_latlon(self):
        # Northern hemisphere
        crs = utm_crs_from_latlon(self.lat, self.lon)
        self.assertEqual(str(crs),"epsg:32613")

        # Sourthern hemisphere
        crs = utm_crs_from_latlon(-1*self.lat, self.lon)
        self.assertEqual(str(crs),"epsg:32713")