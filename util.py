#!/usr/bin/env python

import logging
from debug import logged
from collections import defaultdict
from molecule import Molecule


@logged
def get_atoms(molecules):
    """
    """
    atoms = set([])
    for molecule_list in molecules.values():
        for molecule in molecule_list:
            atoms = atoms.union(molecule.items())
    return atoms


@logged
def load_molecules(input_file):
    """
    Load molecules.
    """
    logging.debug("atoms loading from %s", input_file)
    fi = open(input_file, 'r')
    molecules = defaultdict(list)
    for line in fi.readlines():
        s_molecule = line.strip()
        atoms = Molecule.parse_from_string_to_atoms(s_molecule)
        molecule = Molecule(atoms)
        molecules[molecule.hash_key()].append(molecule)
    return molecules
