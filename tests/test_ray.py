#!/usr/bin/env python3

"""Tests for ray class."""

import sys
import unittest
import numpy as np
import math

from evtech import Ray

class TestRay(unittest.TestCase):
    """Tests for `evtech.ray` package."""

    def setUp(self):
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

    