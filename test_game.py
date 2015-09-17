#!/usr/bin/env python

import unittest
import mock

from game import Game, BOARD_SIZE
from molecule import Molecule


try:
    import __builtin__ as builtins
except ImportError:
    import builtins

H2 = ("H", 2)
Na = ("Na", 1)
Cl = ("Cl", 1)
O2 = ("O", 2)
O = ("O", 1)

NaCl = dict([("Na", 1), ("Cl", 1)])
H2O = dict([("H", 2), ("O", 1)])
H2O2 = dict([("H", 2), ("O", 2)])


class TestGame(unittest.TestCase):
    def test_game_get_atoms(self):
        with mock.patch.object(builtins, 'open', mock.mock_open(read_data='H')):
            game = Game("")
        assert game.get_atoms([Molecule(NaCl), Molecule(H2O)]) == set([("H", 2), ("Na", 1), ("O", 1), ("Cl", 1)])
        assert game.get_atoms([Molecule(H2O), Molecule(H2O2)]) == set([("H", 2), ("O", 1), ("O", 2)])

    def test_game_get_molecules(self):
        assert Game.get_molecules("test.txt") == [Molecule(NaCl), Molecule(H2O)]


    def test_game_main(self):
        atoms = ['H', 'O']
        molecules = [Molecule(H2O), Molecule(H2O2)]
        
        with mock.patch.object(builtins, 'open', mock.mock_open(read_data='H2O2\nH2O\nNaCl')):
            game = Game("", 3)
        with mock.patch('random.choice', side_effect=[O2, H2, O, Na, Cl, H2, O, Na, H2]):
            board = Game.board(3, (H2, O, Na))
        game.board = board

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['0:1 0:2', '1:2 0:0'])):
            assert game.main(board, list(atoms), list(molecules)) == 2

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['0:1', '0:2', '1:2 0:0'])):
            assert game.main(board, list(atoms), list(molecules)) == 2

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['0:1 0:2', KeyboardInterrupt])):
            assert game.main(board, list(atoms), list(molecules)) == 1

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['0:1 1:1', '0:1 0:2', KeyboardInterrupt])):
            assert game.main(board, list(atoms), list(molecules)) == 0

        with mock.patch.object(builtins, 'input', mock.Mock(side_effect=['2:0 2:1', '0:1 1:1', KeyboardInterrupt])):
            assert game.main(board, list(atoms), list(molecules)) == -2

    def test_game_parse_user_input(self):
        assert Game.parse_user_input("1:2") == ((1, 2), )
        assert Game.parse_user_input("1:2 4:3") == ((1, 2), (4, 3))
        
    def test_game_board(self):
        with mock.patch('random.choice', side_effect=[O2, H2, O, Na, Cl, H2, O, Na, H2]):
            assert Game.board(3, (('H', 2), ('O', 1), ('Na', 1))) == (([O2, ''], [H2, ''], [O, '']), ([Na, ''], [Cl, ''], [H2, '']), ([O, ''], [Na, ''], [H2, '']))

    def test_game_find_molecule_in_board(self):
        pass

    def test_game_mark_molecules_in_board(self):
        pass
