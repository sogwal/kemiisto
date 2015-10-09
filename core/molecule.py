#!/usr/bin/env python

import logging

from core.debug import logged
from collections import namedtuple

Atom = namedtuple('Atom', ['atom', 'number'])


class Molecule(str):
    """
    Molecule.
    """
    def __init__(self, *args, **kwargs):
        if self:
            self.atoms = self.parse_from_string_to_atoms(self)

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    @logged
    def is_super_molecule(self, other):
        size = len(other)
        return self.startswith(other) and not self[size:size + 1].isdigit()

    @logged
    def parse_from_string_to_atoms(self, molecule):
        logging.debug("Parsing `%s`", molecule)
        atoms = []
        molecule_iter = iter(molecule)
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
            except StopIteration:
                break
            finally:
                if number:
                    atoms.append(Atom(atom, int(number)))
                else:
                    atoms.append(Atom(atom, 1))

        return atoms
