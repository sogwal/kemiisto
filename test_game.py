#!/usr/bin/env python

import unittest
import mock

from game import Game
from molecule import Molecule

try:
    import __builtin__ as builtins
except ImportError:
    import builtins


NaCl = dict([("Na", 1), ("Cl", 1)])
H2O = dict([("H", 2), ("O", 1)])
H2O2 = dict([("H", 2), ("O", 2)])


class TestGame(unittest.TestCase):
    def test_get_atoms(self):
        with mock.patch.object(builtins, 'open', mock.mock_open(read_data='H')):
            game = Game("")
        assert game.get_atoms([Molecule(NaCl), Molecule(H2O)]) == set([("H", 2), ("Na", 1), ("O", 1), ("Cl", 1)])
        assert game.get_atoms([Molecule(H2O), Molecule(H2O2)]) == set([("H", 2), ("O", 1), ("O", 2)])

    def test_molecule_get_molecules(self):
        assert Game.get_molecules("test.txt") == [Molecule(NaCl), Molecule(H2O)]

    def test_game_main(self):
        atoms = ['H', 'O']
        molecules = [Molecule(H2O), Molecule(H2O2)]
        with mock.patch.object(builtins, 'open', mock.mock_open(read_data='H')):
            game = Game("")
        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2O', 'H2O2'])):
            assert game.main(list(atoms), list(molecules)) == 4

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2', 'H2O', 'H2O2'])):
            assert game.main(list(atoms), list(molecules)) == 3

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2', 'H2O', '2O2', 'H2O2'])):
            assert game.main(list(atoms), list(molecules)) == 0

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2O', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 2

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['H2O', 'H', 'H2O2'])):
            assert game.main(list(atoms), list(molecules)) == 3

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['NaCl', 'H2O', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 0

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['O2', 'NaCl', 'H2O', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == -1

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=[KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == 0

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['NaCl', 'H3O', KeyboardInterrupt])):
            assert game.main(list(atoms), list(molecules)) == -4

    def test_game_parse_user_input(self):
        pass

    def test_game_board(self):
        pass

    def test_game_find_molecule_in_board(self):
        pass

    def test_game_mark_molecules_in_board(self):
        pass
