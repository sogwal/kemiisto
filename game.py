#!/usr/bin/env python
"""
Chemistry game prototyping.
"""

import logging
import random
from util import logged
from molecule import Molecule

BOARD_SIZE = 9

EMPTY = ""
MARKED = "o"
CHECKED = "X"


class Game(object):
    @logged
    def __init__(self, molecules_file):
        self.molecules = self.get_molecules(molecules_file)
        self.atoms = self.get_atoms(self.molecules)
        self.board = self.board(BOARD_SIZE, self.atoms)

    @staticmethod
    @logged
    def get_atoms(molecules):
        """
        """
        atoms = set([])
        for molecule in molecules:
            atoms = atoms.union(molecule.items())
        return atoms

    @staticmethod
    @logged
    def get_molecules(input_file):
        """
        Load molecules.
        """
        logging.debug("atoms loading from %s", input_file)
        fi = open(input_file, 'r')
        molecules = []
        for line in fi.readlines():
            s_molecule = line.strip()
            atoms = Molecule.parse_to_atoms(s_molecule)
            molecules.append(Molecule(atoms))
        return molecules

    @logged
    def main(self, atoms, molecules):
        """
        Main game function.
        """
        score = 0
        print("You have these atoms:", atoms)
        partial_indeces = list()
        # Main game loop
        while molecules:
            self.print_board()
            try:
                s_user_input = input("Create molecule:")
                logging.debug("user input `%s`", s_user_input)
                indeces = self.parse_user_input(s_user_input)
                partial_indeces.extend(indeces)
                user_molecule = self.find_molecule_in_board(partial_indeces)
                try:
                    molecules.pop(molecules.index(user_molecule))
                    self.mark_molecules_in_board(partial_indeces, CHECKED)
                except ValueError:
                    possible_molecules = [molecule
                                          for molecule in molecules
                                          if molecule.issubset(user_molecule)]
                    if possible_molecules:
                        print("You are on the right way")
                        logging.debug("possible molecules %s", possible_molecules)
                        self.mark_molecules_in_board(partial_indeces, MARKED)
                    else:
                        self.mark_molecules_in_board(partial_indeces, EMPTY)
                        partial_indeces = list()
                        score = score - 1
                    print("Try it again")
                else:
                    partial_indeces = list()
                    score = score + 1
                    print("Found it!")
                    logging.debug("left molecules %s", molecules)
                logging.debug("score %s", score)
            except (ValueError, IndexError):
                print("Bad coords inserted!")
                logging.warn("bad coords input `%s`", s_user_input)
            except KeyboardInterrupt:
                break
        else:
            print("You are finished!")
            logging.debug("Empty molecules")
        return score

    @logged
    def board(self, size, atoms):
        board = list()
        atoms = list(atoms)
        for _ in range(BOARD_SIZE):
            row = list()
            for _ in range(BOARD_SIZE):
                rand_atom = atoms[random.randint(0, len(atoms) - 1)]
                row.append([rand_atom, EMPTY])
            board.append(row)

        return board

    @logged
    def print_board(self):
        logging.debug("%s", self.board)
        print("\t\t"+"\t\t".join(str(ind) for ind in range(BOARD_SIZE)))
        print("\t"+"-"*(BOARD_SIZE*(2*7+2)+1))
        for ind, row in enumerate(self.board):
            print("\t%s" % ind + "|\t"+"\t|\t".join("(%s%d)" % r if s == CHECKED else "[%s%d]" % r if s == MARKED else "%s%d" % r for r, s in row)+"\t|")
            print("\t"+"-"*(BOARD_SIZE*(2*7+2)+1))

       # print("\n".join(map("\t|\t".join, self.board)))

    @logged
    def parse_user_input(self, user_input):
        return list(map(lambda x: (int(x[0]), int(x[1])), map(lambda x: x.split(":"), user_input.split(" "))))

    @logged
    def find_molecule_in_board(self, indeces):
        atoms = list()
        for x, y in indeces:
            atoms.append(self.board[x][y][0])
        return Molecule(atoms)

    @logged
    def mark_molecules_in_board(self, indeces, mark):
        for x, y in indeces:
            self.board[x][y][1] = mark

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG)
    # Preparing game
    game = Game(sys.argv[1])
    score = game.main(game.atoms, game.molecules)
    print("Final score:", score)
