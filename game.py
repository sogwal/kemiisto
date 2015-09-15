#!/usr/bin/env python
"""
Chemistry game prototyping.
"""

import logging
from util import logged
from molecule import Molecule


class Game(object):
    @logged
    def __init__(self, molecules_file):
        self.molecules = Molecule.get_molecules(molecules_file)
        self.atoms = self.get_atoms(self.molecules)

    @logged
    def get_atoms(self, molecules):
        """
        """
        atoms = set([])
        for molecule in molecules:
            atoms = atoms.union(molecule.keys())
        return atoms

    @staticmethod
    @logged
    def main(atoms, molecules):
        """
        Main game function.
        """
        score = 0
        print("You have these atoms:", atoms)

        while True:
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
                        continue

                    score = score - 1
                    print("Try it again")
                else:
                    # reset
                    score = score + 1
                    print("Found it!")
                    logging.debug("left molecules %s", molecules)
                logging.debug("score %s", score)
            except (ValueError, StopIteration):
                logging.warn("bad formula input `%s`", s_user_molecule)
                pass
            except KeyboardInterrupt:
                break
        return score


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG)
    # Preparing game
    game = Game(sys.argv[1])
    score = game.main(game.atoms, game.molecules)
    print("Final score:", score)
