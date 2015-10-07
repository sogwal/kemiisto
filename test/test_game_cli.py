#!/usr/bin/env python

import unittest
import mock

from game_cli import Game
from test._dataset import *


try:
    import __builtin__ as builtins
except ImportError:
    import builtins


class TestGame(unittest.TestCase):
    def test_game_parse_user_input(self):
        assert Game.parse_user_input("1:2") == ((1, 2), )
        assert Game.parse_user_input("1:2 4:3") == ((1, 2), (4, 3))


class TestGameMain(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(builtins, 'open', mock.mock_open(
                read_data='H2O\nNaCl')):
            with mock.patch('random.choice',
                            side_effect=[O, H2, O, Na, Cl, H2, O, Na, H2]):
                self.game = Game("", 3)

    def test_game_main1(self):
        with mock.patch.object(builtins, 'input', mock.Mock(
                side_effect=['0:1 0:2', '1:0 1:1', KeyboardInterrupt])):
            # temporary with KeyboardInterrupt
            assert self.game.main() == 2

    def test_game_main2(self):
        with mock.patch.object(builtins, 'input', mock.Mock(
                side_effect=['0:1', '0:2', '1:0 1:1', KeyboardInterrupt])):
            # temporary with KeyboardInterrupt
            assert self.game.main() == 2

    def test_game_main3(self):
        with mock.patch.object(builtins, 'input', mock.Mock(
                side_effect=['0:1 0:2', KeyboardInterrupt])):
            assert self.game.main() == 1

    def test_game_main4(self):
        with mock.patch.object(builtins, 'input', mock.Mock(
                side_effect=['0:1 1:1', '0:1 0:2', KeyboardInterrupt])):
            assert self.game.main() == 0

    def test_game_main5(self):
        with mock.patch.object(builtins, 'input', mock.Mock(
                side_effect=['2:0 2:1', '0:1 1:1', KeyboardInterrupt])):
            assert self.game.main() == -2
