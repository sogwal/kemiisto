#!/usr/bin/env python

import unittest
from molecule import Molecule
from test_dataset import *


class TestMolecule(unittest.TestCase):
    def test_molecule_parse_from_string_to_atoms(self):
        assert Molecule.parse_from_string_to_atoms("NaCl") == NaCl
        assert Molecule.parse_from_string_to_atoms("H2O") == H2O
        assert Molecule.parse_from_string_to_atoms("H2O2") == H2O2
        assert Molecule.parse_from_string_to_atoms("H2SO4") == H2SO4

    def test_molecule_issubset(self):
        assert Molecule(NaCl).issubset(Molecule([Na])) == True
        assert Molecule(NaCl).issubset(Molecule([Na, Cl])) == True
        assert Molecule(NaCl).issubset(Molecule([Na2, Cl])) == False
        assert Molecule(H2O).issubset(Molecule(H2O2)) == False
        assert Molecule(H2O2).issubset(Molecule(H2O)) == True
        assert Molecule(H2O).issubset(Molecule([H2])) == True

    @unittest.skip
    def test_molecule_hash_key(self):
        raise
