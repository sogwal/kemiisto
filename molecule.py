#!/usr/bin/env python

import logging

from util import logged
from collections import defaultdict

class Molecule(dict):
    """
    """
    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, super(Molecule, self))

    @logged
    def issubset(self, other):
        logging.debug("issubset")
        for atom, number in other.items():
            if atom not in self or number > self[atom]:
                return False

        return True

    @staticmethod
    @logged
    def parse_to_atoms(molecule):
        logging.debug("Parsing `%s`", molecule)
        atoms = defaultdict(int)
        molecule = iter(molecule)
        c = next(molecule)
        while True:
            atom = ""
            number = ""
            try:

                if c.isupper():
                    atom = c
                else:
                    raise ValueError("mismatch formula")

                c = next(molecule)
                if c.islower():
                    atom = atom + c
                    c = next(molecule)
                    if c.islower():
                        atom = atom + c
                        c = next(molecule)

                if c.isdigit():
                    number = c

                    c = next(molecule)
                    while True:
                        if c.isdigit():
                            number = number + c
                        else:
                            break
            except StopIteration:
                break
            finally:
                if number:
                    atoms[atom] += int(number)
                else:
                    atoms[atom] += 1

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
