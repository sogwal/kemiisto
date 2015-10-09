#!/usr/bin/env python
from core.debug import logged
import logging
from core.molecule import Molecule


class MissingError(BaseException):
    pass


class Storage(list):
    @classmethod
    @logged
    def load_molecules(cls, input_file):
        """
        Load molecules.
        """
        logging.debug("atoms loading from %s", input_file)
        fi = open(input_file, 'r')
        molecules = cls()
        for line in fi.readlines():
            molecule = line.strip()
            molecules.append(Molecule(molecule))
        return molecules

    @logged
    def get_atoms(self):
        """
        """
        atoms = set([])
        for molecule in self:
            atoms = atoms.union(set(molecule.atoms))
        return atoms

    @logged
    def get_super_molecules(self, other):
        return [molecule for molecule in self
                if molecule.is_super_molecule(other)]

    @logged
    def find(self, molecule):
        try:
            self.index(molecule)
        except ValueError:
            raise MissingError
