#!/usr/bin/env python
import unittest
from molecule import Molecule
import util
from test_dataset import *


class TestUtils(unittest.TestCase):
    def test_game_get_atoms(self):
        assert util.get_atoms(dict(ClNa=[Molecule(NaCl)], HO=[Molecule(H2O)])) == \
            set([("H", 2), ("Na", 1), ("O", 1), ("Cl", 1)])
        assert util.get_atoms(dict(HO=[Molecule(H2O), Molecule(H2O2)])) == \
            set([("H", 2), ("O", 1), ("O", 2)])

    def test_game_load_molecules(self):
        assert util.load_molecules("test/test.txt") == \
            dict(ClNa=[Molecule(NaCl)], HO=[Molecule(H2O)])
