#!/usr/bin/env python

import logging

from core.debug import logged
from collections import defaultdict


class Molecule(defaultdict):
    """
    Molecule.
    """
    def __init__(self, *args, **kwargs):
        super(Molecule, self).__init__(int, *args, **kwargs)

    def __repr__(self):
        return "%s%s" % (self.__class__.__name__, self.items())

    @logged
    def is_super_molecule(self, other):
        for atom, number in other.items():
            if atom not in self or number > self[atom]:
                return False

        return True

    @classmethod
    @logged
    def parse_from_string_to_atoms(cls, molecule_string):
        logging.debug("Parsing `%s`", molecule_string)
        molecule = cls()
        molecule_iter = iter(molecule_string)
        c = next(molecule_iter)
        while True:
            atom = ""
            number = ""
            try:

                if c.isupper():
                    atom = c
                else:
                    raise ValueError("mismatch formula")

                c = next(molecule_iter)
                if c.islower():
                    atom = atom + c
                    c = next(molecule_iter)
                    if c.islower():
                        atom = atom + c
                        c = next(molecule_iter)

                if c.isdigit():
                    number = c

                    c = next(molecule_iter)
                    while True:
                        if c.isdigit():
                            number = number + c
                        else:
                            break
            except StopIteration:
                break
            finally:
                if number:
                    molecule[atom] += int(number)
                else:
                    molecule[atom] += 1

        return molecule
