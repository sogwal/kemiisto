#!/usr/bin/env python
import unittest
from core.storage import Storage
from core.molecule import Molecule
from test._dataset import *


class TestStorage(unittest.TestCase):
    def test_storage_get_atoms(self):
        storage = Storage([Molecule("NaCl"), Molecule("H2O"),
                           Molecule("H2O2")])
        assert storage.get_atoms() == \
            set([("H", 2), ("Na", 1), ("O", 1), ("Cl", 1), ("O", 2)])

    def test_storage_load_molecules(self):
        assert Storage.load_molecules("test/test.txt") == \
            [Molecule("NaCl"), Molecule("H2O")]

    def test_storage_get_super_molecules(self):
        from nose import SkipTest
        raise SkipTest

    def test_storage_find(self):
        from nose import SkipTest
        raise SkipTest
