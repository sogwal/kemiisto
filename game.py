#!/usr/bin/env python
"""
Chemistry game prototyping.
"""

import logging
import random
from util import logged
from molecule import Molecule

BOARD_SIZE = 9

class Game(object):
    @logged
    def __init__(self, molecules_file):
        self.molecules = Molecule.get_molecules(molecules_file)
        self.atoms = self.get_atoms(self.molecules)
        self.board = self.board(BOARD_SIZE, self.atoms)

    @logged
    def get_atoms(self, molecules):
        """
        """
        atoms = set([])
        for molecule in molecules:
            atoms = atoms.union(molecule.items())
        return atoms

    @staticmethod
    @logged
    def main(atoms, molecules):
        """
        Main game function.
        """
        score = 0
        print("You have these atoms:", atoms)

        while molecules:
            # Main game loop
            try:
                s_user_molecule = input("Create molecule:")
                logging.debug("user input `%s`", s_user_molecule)
                # check input
                user_molecule = Molecule.parse_to_atoms(s_user_molecule)
                try:
                    molecules.pop(molecules.index(user_molecule))
                except ValueError:
                    possible_molecules = [molecule
                                          for molecule in molecules
                                          if molecule.issubset(user_molecule)]
                    if possible_molecules:
                        print("You are on the right way")
                        logging.debug("possible molecules %s", possible_molecules)
                        score = score - 1
                    else:
                        score = score - 2
                    print("Try it again")
                else:
                    score = score + 2
                    print("Found it!")
                    logging.debug("left molecules %s", molecules)
                logging.debug("score %s", score)
            except (ValueError, StopIteration):
                logging.warn("bad formula input `%s`", s_user_molecule)
                score = score - 3
                pass
            except KeyboardInterrupt:
                break
        else:
            logging.debug("Empty molecules")
            print("You are finished!")
        return score

    @logged
    def board(self, size, atoms):
        board = list()
        atoms = list(atoms)
        for _ in range(BOARD_SIZE):
            row = list()
            for _ in range(BOARD_SIZE):
                rand_atom = atoms[random.randint(0, len(atoms) - 1)]
                row.append(rand_atom)
            board.append(row)

        return board

    @logged
    def print_board(self):
        print("-"*(BOARD_SIZE*(2*7+2)+1))
        for row in self.board:
            print("|\t"+"\t|\t".join(row)+"\t|")
            print("-"*(BOARD_SIZE*(2*7+2)+1))

       # print("\n".join(map("\t|\t".join, self.board)))


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG)
    # Preparing game
    game = Game(sys.argv[1])
    game.print_board()
    score = game.main(game.atoms, game.molecules)
    print("Final score:", score)
