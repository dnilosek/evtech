#!/usr/bin/env python3

"""Tests for dataset functions"""

import unittest

from pathlib import Path

from evtech import load_dataset
from evtech import Camera

from .test_util import rmtree

def mock_loader(json_path, image_path):
    # Return an empty camera with image path
    return Camera(None,None,None,None,None,None,image_path)

class TestDataset(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        self.tmp = Path("temp/")
        self.nadirs = self.tmp.joinpath("nadirs")
        self.obliques = self.tmp.joinpath("obliques")
        self.nadirs.mkdir(parents=True, exist_ok=True)
        self.obliques.mkdir(parents=True, exist_ok=True)

        # Make fake data
        self.nadirs.joinpath("test.jpg").touch()
        self.nadirs.joinpath("test.json").write_text("{}")
        self.obliques.joinpath("test.jpg").touch()
        self.obliques.joinpath("test.json").write_text("{}")
        pass

    def tearDown(self):
        rmtree(self.tmp)
        pass

    def test_load_dataset(self):

        nadirs, obliques = load_dataset(self.tmp, mock_loader)
        
        self.assertEqual(1,len(nadirs))
        self.assertEqual(1,len(obliques))

        self.assertEqual(self.nadirs.joinpath("test.jpg"), nadirs[0].image_path)
        self.assertEqual(self.obliques.joinpath("test.jpg"), obliques[0].image_path)