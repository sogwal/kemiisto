#!/usr/bin/env python

import logging

from util import logged


class Molecule(dict):
    """
    """
    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self)

    def issubset(self, other):
        for atom, number in other.items():
            if atom not in self or number > self[atom]:
                return False

        return True

    @staticmethod
    @logged
    def parse_to_atoms(molecule):
        atoms = dict()
        atom = ""
        number = ""
        molecule = iter(molecule)
        c = next(molecule)
        while True:
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
                    number = number + c
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
                    atoms[atom] = int(number)
                else:
                    atoms[atom] = 1
                atom = ""
                number = ""

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
