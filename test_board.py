#!/usr/bin/env python

import unittest
import mock

from board import Board
from molecule import Molecule
from test_dataset import *


class TestBoard(unittest.TestCase):
    def test_board_generate(self):
        with mock.patch('random.choice', side_effect=[O2, H2, O, Na, Cl, H2, O, Na, H2]):
            assert Board.generate(3, (H2, O, Na)) == Board((([O2, ''], [H2, ''], [O, '']),
                                                            ([Na, ''], [Cl, ''], [H2, '']),
                                                            ([O, ''], [Na, ''], [H2, ''])), 3)

    def test_game_find_molecule_in_board(self):
        with mock.patch('random.choice', side_effect=[O2, H2, O, Na, Cl, H2, O, Na, H2]):
            board = Board.generate(3, (H2, O, Na))
            assert board.find_molecule_in_board(((0, 1), (0, 2))) == Molecule(H2O)

    def test_game_mark_molecules_in_board(self):
        with mock.patch('random.choice', side_effect=[O2, H2, O, Na, Cl, H2, O, Na, H2]):
            board = Board.generate(3, (H2, O, Na))
            board.mark_molecules_in_board(((0, 1), (0, 2)), "X")
            assert board == (([O2, ''], [H2, 'X'], [O, 'X']),
                             ([Na, ''], [Cl, ''], [H2, '']),
                             ([O, ''], [Na, ''], [H2, '']))
