#!/usr/bin/env python
import unittest
from core.storage import HashedStorage
from core.molecule import Molecule
from test._dataset import *


class TestHashedStorage(unittest.TestCase):
    def test_hashedstorage_get_atoms(self):
        storage = HashedStorage(dict(ClNa=[Molecule(NaCl)],
                                HO=[Molecule(H2O), Molecule(H2O2)]))
        assert storage.get_atoms() == \
            set([("H", 2), ("Na", 1), ("O", 1), ("Cl", 1), ("O", 2)])

    def test_hashedstorage_load_molecules(self):
        assert HashedStorage.load_molecules("test/test.txt") == \
            dict([(frozenset(['Cl', 'Na']), [Molecule(NaCl)]),
                  (frozenset(['H', 'O']), [Molecule(H2O)])])
