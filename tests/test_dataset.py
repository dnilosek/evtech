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
        self.nadirs.joinpath("0.jpg").touch()
        self.nadirs.joinpath("0.json").touch()
        self.nadirs.joinpath("1.jpg").touch()
        self.nadirs.joinpath("1.json").touch()
        self.obliques.joinpath("0.jpg").touch()
        self.obliques.joinpath("0.json").touch()
        self.obliques.joinpath("1.jpg").touch()
        self.obliques.joinpath("1.json").touch()
        self.obliques.joinpath("2.jpg").touch()
        self.obliques.joinpath("2.json").touch()
        pass

    def tearDown(self):
        rmtree(self.tmp)
        pass

    def test_load_dataset(self):

        load_dataset(self.tmp, mock_loader)