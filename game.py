#!/usr/bin/env python
"""
Chemistry game prototyping.
"""

import logging
import functools


def logged(func):
    @functools.wraps(func)
    def with_logging(*args, **kwargs):
        s_args = ", ".join(map(str, args))
        s_kwargs = ", ".join("%s=%s" % kwarg for kwarg in kwargs.items())
        logging.debug("Calling %s(%s, %s)", func.__name__, s_args, s_kwargs)
        retval = func(*args, **kwargs)
        logging.debug("Returning %s(%s, %s) = %s", func.__name__, s_args, s_kwargs, retval)
        return retval
    return with_logging


@logged
def parse_to_atoms(molecule):
    atoms = []
    atom = ""
    molecule = iter(molecule)
    c = next(molecule)
    while True:
        try:
            if c.isupper():
                atom = c
            else:
                raise ValueError(c)

            c = next(molecule)
            if c.islower():
                atom = atom + c
                c = next(molecule)
                if c.islower():
                    atom = atom + c
                    c = next(molecule)

            if c.isdigit():
                c = next(molecule)
                while True:
                    if c.isdigit():
                        pass
                    else:
                        break
        except StopIteration:
            break
        finally:
            atoms.append(atom)
            atom = ""

    return atoms            


@logged
def get_atoms(molecules):
    """
    Parse atoms.
    """
    atoms = set([])
    for molecule in molecules:
        atoms = atoms.union(set(parse_to_atoms(molecule)))
    return atoms


@logged
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
        print(parse_to_atoms(molecule))
    return molecules


@logged
def main(atoms, molecules):
    """
    Main game function.
    """
    score = 0
    print("You have these atoms:", atoms)

    possible_molecules = molecules
    while True:
        # Main game loop
        try:
            user_molecule = input("Create molecule:")
            logging.debug("user input `%s`", user_molecule)

            try:
                molecules.pop(possible_molecules.index(user_molecule))
            except ValueError:
                possible_molecules = [molecule
                                      for molecule in possible_molecules
                                      if molecule.find(user_molecule) != -1]
                if possible_molecules:
                    print("You are on the right way")
                    logging.debug("possible molecules %s", possible_molecules)
                    continue

                # reset
                possible_molecules = molecules
                score = score - 1
                print("Try it again")
            else:
                # reset
                possible_molecules = molecules
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
    molecules = get_molecules(sys.argv[1])
    atoms = get_atoms(molecules)
    score = main(atoms, molecules)
    print("Final score:", score)
