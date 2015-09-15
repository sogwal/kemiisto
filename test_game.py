#!/usr/bin/env python

import unittest
import mock

from game import Game
from molecule import Molecule
# get_atoms, get_molecules, game.main

try:
    import __builtin__ as builtins
except ImportError:
    import builtins


NaCl = dict([("Na", 1), ("Cl", 1)])
H2O = dict([("H", 2), ("O", 1)])
H2O2 = dict([("H", 2), ("O", 2)])


class TestGame(unittest.TestCase):
    def test_get_atoms(self):
        with mock.patch.object(builtins, 'open', mock.mock_open(read_data='')):
            game = Game("")
        assert game.get_atoms([Molecule(NaCl), Molecule(H2O)]) == set(["H", "Na", "O", "Cl"])
        assert game.get_atoms([Molecule(H2O), Molecule(H2O2)]) == set(["H", "O"])

    def test_game_main(self):
        atoms = ['H', 'O']
        molecules = [Molecule(H2O), Molecule(H2O2)]
        with mock.patch.object(builtins, 'open', mock.mock_open(read_data='')):
            game = Game("")
        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2O', 'H2O2', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 2

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2', 'H2O', 'H2O2', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 2

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2', 'H2O', '2O2', 'H2O2', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 2

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2O', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 1

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2O', 'H2O2', 'H', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 1

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['NaCl', 'H2O', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 0

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['O2', 'NaCl', 'H2O', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 0

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=[KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 0

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['NaCl', 'H3O', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == -2
