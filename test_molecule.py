#!/usr/bin/env python


import unittest
from collections import OrderedDict

from molecule import Molecule


NaCl = OrderedDict([("Na", 1), ("Cl", 1)])
H2O = OrderedDict([("H", 2), ("O", 1)])
H2O2 = OrderedDict([("H", 2), ("O", 2)])
H2SO4 = OrderedDict([("H", 2), ("S", 1), ("O", 4)])


class TestMolecule(unittest.TestCase):

    def test_molecule_get_molecules(self):
        assert Molecule.get_molecules("test.txt") == [Molecule(NaCl), Molecule(H2O)]

    def test_molecule_parse_to_atoms(self):
        assert Molecule.parse_to_atoms("NaCl") == NaCl
        assert Molecule.parse_to_atoms("H2O") == H2O
        assert Molecule.parse_to_atoms("H2O2") == H2O2
        assert Molecule.parse_to_atoms("H2SO4") == H2SO4
