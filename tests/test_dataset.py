#!/usr/bin/env python3

"""Tests for dataset functions"""

import unittest

from pathlib import Path

from evtech import load_dataset
from .test_util import rmtree

class TestDataset(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        self.tmp = Path("temp/")
        self.tmp.mkdir(parents=True, exist_ok=True)

        pass

    def tearDown(self):
        #rmtree(self.tmp)
        pass

    def test_load_dataset(self):

        load_dataset(self.tmp)