#!/usr/bin/env python

import unittest
import mock
import builtins

from game import get_atoms, get_molecules, main


class TestGame(unittest.TestCase):
    def test_get_atoms(self):
        assert get_atoms("H,N,O") == ["H", "N", "O"]
        assert get_atoms("H,Na,O") == ["H", "Na", "O"]

    def test_get_molecules(self):
        assert get_molecules("test.txt") == ["NaCl", "H2O"]

    def test_main(self):
        atoms = ['H', 'O']
        molecules = ['H2O', 'H2O2']
        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2O', 'H2O2', KeyboardInterrupt])):
            assert main(atoms.copy(), molecules.copy()) == 2

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2O', KeyboardInterrupt])):
            assert main(atoms.copy(), molecules.copy()) == 1

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['NaCl', 'H2O', KeyboardInterrupt])):
            assert main(atoms.copy(), molecules.copy()) == 0

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=[KeyboardInterrupt])):
            assert main(atoms.copy(), molecules.copy()) == 0

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['NaCl', 'H3O', KeyboardInterrupt])):
            assert main(atoms.copy(), molecules.copy()) == -2