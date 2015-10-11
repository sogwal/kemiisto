#!/usr/bin/env python

import unittest
import mock

from core.board import Board, BoardItem, BoardItemStatus, I
from test._dataset import *


class TestBoard(unittest.TestCase):
    def test_board_generate(self):
        with mock.patch('random.choice',
                        side_effect=[O, H2, O, Na, H2, H2, O, Na, H2]):
            board = Board([], 0)
            board.generate(3, (H2, O, Na))
            assert board.iterable == \
                [BoardItem(O, I(0, 0)), BoardItem(H2, I(0, 1)),
                 BoardItem(O, I(0, 2)),
                 BoardItem(Na, I(1, 0)), BoardItem(H2, I(1, 1)),
                 BoardItem(H2, I(1, 2)),
                 BoardItem(O, I(2, 0)), BoardItem(Na, I(2, 1)),
                 BoardItem(H2, I(2, 2))]

    def test_board_find_molecule_in_board(self):
        board = Board([BoardItem(O, I(0, 0)), BoardItem(H2, I(0, 1)),
                       BoardItem(O, I(0, 2)),
                       BoardItem(Na, I(1, 0)), BoardItem(H2, I(1, 1)),
                       BoardItem(H2, I(1, 2)),
                       BoardItem(O, I(2, 0)), BoardItem(Na, I(2, 1)),
                       BoardItem(H2, I(2, 2))], 3)
        assert board.find_molecule_in_board((I(0, 1), I(0, 2))) == "H2O"

    def test_board_mark_molecules_in_board(self):
        board = Board([BoardItem(O, I(0, 0)), BoardItem(H2, I(0, 1)),
                       BoardItem(O, I(0, 2)),
                       BoardItem(Na, I(1, 0)), BoardItem(H2, I(1, 1)),
                       BoardItem(H2, I(1, 2)),
                       BoardItem(O, I(2, 0)), BoardItem(Na, I(2, 1)),
                       BoardItem(H2, I(2, 2))], 3)
        board.mark_molecules_in_board((I(0, 1), I(0, 2)))
        assert board.iterable == \
            [BoardItem(O, I(0, 0)),
             BoardItem(H2, I(0, 1), BoardItemStatus.CHECKED),
             BoardItem(O, I(0, 2), BoardItemStatus.CHECKED),
             BoardItem(Na, I(1, 0)), BoardItem(H2, I(1, 1)),
             BoardItem(H2, I(1, 2)),
             BoardItem(O, I(2, 0)), BoardItem(Na, I(2, 1)),
             BoardItem(H2, I(2, 2))]

    def test_board_neigbours(self):
        with mock.patch('random.choice',
                        side_effect=[O2, H2, O, Na, Cl, H2, O, Na, H2]):
            board = Board([], 0)
            board.generate(3, (H2, O, Na))
            assert board.neighbours(I(1, 1), I(0, 1)) is True
            assert board.neighbours(I(1, 0), I(1, 1)) is True
            assert board.neighbours(I(1, 1), I(2, 1)) is True
            assert board.neighbours(I(1, 2), I(1, 1)) is True

            assert board.neighbours(I(1, 0), I(0, 1)) is False
            assert board.neighbours(I(0, 1), I(0, 1)) is False

    def test_board_is_path(self):
        board = Board([], 0)
        assert board.is_path(I(1, 1), I(0, 1)) is True
        assert board.is_path(I(1, 1), I(0, 1), I(0, 0)) is True
        assert board.is_path(I(1, 1), I(0, 1), I(0, 0), I(2, 1)) is False
        assert board.is_path(I(1, 1), I(0, 0)) is False
        assert board.is_path(I(2, 2), I(0, 0)) is False

    def test_board_all_marked(self):
        from nose import SkipTest
        raise SkipTest

    def test_board_index(self):
        from nose import SkipTest
        raise SkipTest
