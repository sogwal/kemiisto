#!/usr/bin/env python3

import unittest

from game import get_atoms, get_molecules, main


class TestGame(unittest.TestCase):
    def test_get_atoms(self):
        assert get_atoms("H,N,O") == ["H", "N", "O"]
        assert get_atoms("H,Na,O") == ["H", "Na", "O"]

    def test_get_molecules(self):
        assert get_molecules("test.txt") == ["NaCl", "H2O"]

    @unittest.skip
    def test_main(self):
        atoms = []
        molecules = []