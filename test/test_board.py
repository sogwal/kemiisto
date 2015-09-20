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

    def test_board_find_molecule_in_board(self):
        with mock.patch('random.choice', side_effect=[O2, H2, O, Na, Cl, H2, O, Na, H2]):
            board = Board.generate(3, (H2, O, Na))
            assert board.find_molecule_in_board(((0, 1), (0, 2))) == Molecule(H2O)

    def test_board_mark_molecules_in_board(self):
        with mock.patch('random.choice', side_effect=[O2, H2, O, Na, Cl, H2, O, Na, H2]):
            board = Board.generate(3, (H2, O, Na))
            board.mark_molecules_in_board(((0, 1), (0, 2)), "X")
            assert board == (([O2, ''], [H2, 'X'], [O, 'X']),
                             ([Na, ''], [Cl, ''], [H2, '']),
                             ([O, ''], [Na, ''], [H2, '']))

    def test_board_neigbours(self):
        with mock.patch('random.choice', side_effect=[O2, H2, O, Na, Cl, H2, O, Na, H2]):
            board = Board.generate(3, (H2, O, Na))
            assert board.neighbours((1, 1), (0, 1)) == True
            assert board.neighbours((1, 0), (1, 1)) == True
            assert board.neighbours((1, 1), (2, 1)) == True
            assert board.neighbours((1, 2), (1, 1)) == True

            assert board.neighbours((1, 0), (0, 1)) == False
            assert board.neighbours((0, 1), (0, 1)) == False

    def test_board_is_path(self):
        board = Board([], 0)
        assert board.is_path((1, 1), (0, 1)) == True
        assert board.is_path((1, 1), (0, 1), (0, 0)) == True
        assert board.is_path((1, 1), (0, 1), (0, 0), (2, 1)) == False
        assert board.is_path((1, 1), (0, 0)) == False
        assert board.is_path((2, 2), (0, 0)) == False

    def test_board_all_marked(self):
        raise
