#!/usr/bin/env python3
"""
Chemistry game prototyping.
"""

import logging


ATOMS = "H,Cl,Na,S,O,N,C"


def get_atoms(atoms):
    """
    Parse atoms.
    """
    return atoms.split(',')


def get_molecules(input_file):
    """
    Load molecules.
    """
    logging.debug("atoms loading from %s", input_file)
    fi = open(input_file, 'r')
    molecules = []
    for line in fi.readlines():
        molecule = line.strip()
        molecules.append(molecule)
    return molecules


def main(atoms, molecules):
    """
    Main game function.
    """
    score = 0
    print("You have these atoms:", atoms)
    while True:
        # Main game loop
        try:
            user_molecule = input("Create molecule:")
            logging.debug("user input `%s`", user_molecule)
            try:
                molecules.pop(molecules.index(user_molecule))
            except ValueError:
                score = score - 1
                print("Try it again")
            else:
                score = score + 1
                print("Found it!")
                logging.debug("left molecules %s", molecules)
            logging.debug("score %s", score)
        except KeyboardInterrupt:
            break
    return score


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG)
    # Preparing game
    atoms = get_atoms(ATOMS)
    molecules = get_molecules(sys.argv[1])
    score = main(atoms, molecules)
    print("Final score:", score)
