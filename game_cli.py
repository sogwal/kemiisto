#!/usr/bin/env python
"""
Chemistry game prototyping.
"""

import logging
from core.debug import logged
from core.board import Board
from core.board import BoardItemStatus
from core.storage import HashedStorage, MissingError

BOARD_SIZE = 5

import sys
if sys.version_info.major == 2:
    input = raw_input


def print_board(board):
    """Really unreadeable function :-)"""
    logging.debug("%s", str(board))
    print("\t\t" + "\t\t".join(str(ind) for ind in range(board.size)))
    print("\t" + "-" * (board.size * (2 * 7 + 2) + 1))
    for ind in range(board.size):
        print("\t%s" % ind + "|\t" + "\t|\t".join("(%s%d)" % (r.atom, r.count)
              if r.status == BoardItemStatus.CHECKED else "[%s%d]" %
              (r.atom, r.count)
              if r.status == BoardItemStatus.MARKED else "%s%d" %
              (r.atom, r.count)
              for r in board[ind * board.size:(ind + 1) * board.size]) +
              "\t|")
    print("\t" + "-" * (board.size * (2 * 7 + 2) + 1))


class Game(object):
    @logged
    def __init__(self, molecules_file, board_size):
        self.storage = HashedStorage.load_molecules(molecules_file)
        atoms = self.storage.get_atoms()
        self.board = Board.generate(board_size, atoms)

    @logged
    def main(self):
        """
        Main game function.
        """
        score = 0
        partial_indeces = list()
        # Main game loop
        while not self.board.all_marked():
            print_board(self.board)
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
                continue

            try:
                self.storage.find(user_molecule)
                self.board.mark_molecules_in_board(partial_indeces,
                                                   BoardItemStatus.CHECKED)
            except MissingError:
                possible_molecules = self.storage.\
                    get_super_molecules(user_molecule)
                if possible_molecules:
                    print("You are on the right way")
                    logging.debug("possible molecules %s", possible_molecules)
                    self.board.mark_molecules_in_board(partial_indeces,
                                                       BoardItemStatus.MARKED)
                else:
                    self.board.mark_molecules_in_board(partial_indeces,
                                                       BoardItemStatus.EMPTY)
                    partial_indeces = list()
                    score = score - 1
                print("Try it again")
            except IndexError:
                self.board.mark_molecules_in_board(partial_indeces,
                                                   BoardItemStatus.EMPTY)
                partial_indeces = list()
                score = score - 1
                print("Try it again!")
            else:
                partial_indeces = list()
                score = score + 1
                print("Found it!")
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
