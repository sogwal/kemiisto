#!/usr/bin/env python

import logging

from util import logged
from collections import defaultdict


class Molecule(dict):
    """
    """
    @logged
    def issubset(self, other):
        logging.debug("issubset")
        for atom, number in other.items():
            if atom not in self or number > self[atom]:
                return False

        return True

    @staticmethod
    @logged
    def parse_from_string_to_atoms(molecule):
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

    def hash_key(self):
        return "".join(sorted(self.keys()))
