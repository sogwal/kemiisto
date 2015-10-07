#!/usr/bin/env python
from core.debug import logged
from collections import defaultdict, namedtuple
import logging
from core.molecule import Molecule

Atom = namedtuple('Atom', ['atom', 'count'])


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
            s_molecule = line.strip()
            molecule = Molecule.parse_from_string_to_atoms(s_molecule)
            molecules.append(molecule)
        return molecules

    @logged
    def get_atoms(self):
        """
        """
        atoms = set([])
        for molecule in self:
            atoms = atoms.union([Atom(*mol) for mol in molecule.items()])

        return atoms

    @logged
    def get_submolecules(self, other):
        return [molecule for molecule in self
                if molecule.is_super_molecule(other)]

    @logged
    def find(self, molecule):
        try:
            self.index(molecule)
        except IndexError:
            raise MissingError


class HashedStorage(defaultdict):
    hash_key = lambda molecule: frozenset(molecule)

    def __init__(self, *args, **kwargs):
        super(HashedStorage, self).__init__(list, *args, **kwargs)

    # def __repr__(self):
    #    return "<%s(%s)>" % (self.__class__.__name__, self.keys())

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
            s_molecule = line.strip()
            molecule = Molecule.parse_from_string_to_atoms(s_molecule)
            molecules[cls.hash_key(molecule.keys())].append(molecule)
        return molecules

    @logged
    def get_atoms(self):
        """
        """
        atoms = set([])
        for molecule_list in self.values():
            for molecule in molecule_list:
                atoms = atoms.union([Atom(*mol) for mol in molecule.items()])
        return atoms

    @logged
    def get_super_molecules(self, other):
        submolecules = []
        hashkey = HashedStorage.hash_key(other)
        for key, molecules in self.items():
            if key.issuperset(hashkey):
                submolecules.extend([molecule for molecule in molecules
                                     if molecule.is_super_molecule(other)])
        return submolecules

    @logged
    def find(self, molecule):
        hashkey = HashedStorage.hash_key(molecule)
        if hashkey not in self:
            raise MissingError
        try:
            self[hashkey].index(molecule)
        except IndexError:
            raise MissingError
