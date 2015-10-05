#!/usr/bin/env python
"""
Chemistry game prototyping.
"""

import logging
from debug import logged
from util import get_atoms, load_molecules

from board import Board, EMPTY, MARKED, CHECKED

BOARD_SIZE = 5


class Game(object):
    @logged
    def __init__(self, molecules_file, board_size):
        self.molecules = load_molecules(molecules_file)
        atoms = get_atoms(self.molecules)
        self.board = Board.generate(board_size, atoms)

    @logged
    def main(self):
        """
        Main game function.
        """
        score = 0
        partial_indeces = list()
        # Main game loop
        while not self.board.all_marked(CHECKED):
            self.board.print_board()
            try:
                s_user_input = input("Create molecule:")
                logging.debug("user input `%s`", s_user_input)
            except KeyboardInterrupt:
                break

            try:
                indeces = self.parse_user_input(s_user_input)
                try:
                    if not self.board.is_path(partial_indeces[-1], *indeces):
                        raise ValueError
                except IndexError:
                    pass
                partial_indeces.extend(indeces)
                user_molecule = self.board.\
                    find_molecule_in_board(partial_indeces)
            except (ValueError, IndexError):
                print("Bad coords inserted!")
                logging.warn("bad coords input `%s`", s_user_input)

            try:
                molecules = self.molecules[user_molecule.hash_key()]
                molecules.index(user_molecule)
                self.board.mark_molecules_in_board(partial_indeces, CHECKED)
            except ValueError:
                possible_molecules = [molecule
                                      for molecule in molecules
                                      if molecule.issubset(user_molecule)]
                if possible_molecules:
                    print("You are on the right way")
                    logging.debug("possible molecules %s", possible_molecules)
                    self.board.mark_molecules_in_board(partial_indeces, MARKED)
                else:
                    self.board.mark_molecules_in_board(partial_indeces, EMPTY)
                    partial_indeces = list()
                    score = score - 1
                print("Try it again")
            except IndexError:
                self.board.mark_molecules_in_board(partial_indeces, EMPTY)
                partial_indeces = list()
                score = score - 1
                print("Try it again")
            else:
                partial_indeces = list()
                score = score + 1
                print("Found it!")
                logging.debug("left molecules %s", self.molecules)
            logging.debug("score %s", score)

        else:
            print("You are finished!")
            logging.debug("Empty molecules")
        return score

    @staticmethod
    @logged
    def parse_user_input(user_input):
        return tuple(map(lambda x: (int(x[0]), int(x[1])),
                         map(lambda x: x.split(":"),
                             user_input.strip().split(" "))))


if __name__ == "__main__":
    import sys
    format = "%(asctime)-15s %(name)s %(levelname)-8s %(message)s \
              [%(filename)s.%(funcName)s:%(lineno)s]"
    logging.basicConfig(level=logging.DEBUG, format=format)
    # Preparing game
    game = Game(sys.argv[1], BOARD_SIZE)
    score = game.main()
    print("Final score:", score)
