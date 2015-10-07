#!/usr/bin/env python
from core.debug import logged
from collections import defaultdict, namedtuple
import logging
from core.molecule import Molecule


hash_key = lambda molecule: frozenset(molecule)

Atom = namedtuple('Atom', ['atom', 'count'])


class Storage(defaultdict):

    def __init__(self, *args, **kwargs):
        super(Storage, self).__init__(list, *args, **kwargs)

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
            molecules[hash_key(molecule.keys())].append(molecule)
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
    def get_submolecules(self, molecule):
        submolecules = []
        hashkey = hash_key(molecule)
        for key, value in self.items():
            if key.issuperset(hashkey):
                submolecules.extend(value)
        return submolecules
