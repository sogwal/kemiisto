#!/usr/bin/env python

import logging
import random
from util import logged
from molecule import Molecule

EMPTY = ""
MARKED = "o"
CHECKED = "X"


class Board(tuple):
    def __new__(cls, iterable, size):
        self = tuple.__new__(cls, iterable)
        self.size = size
        return self

    @staticmethod
    @logged
    def generate(size, atoms):
        atoms = list(atoms)
        return Board(tuple(
                           tuple([random.choice(atoms), EMPTY]
                                 for _ in range(size))
                           for _ in range(size)), size)

    @logged
    def print_board(self):
        logging.debug("%s", self)
        print("\t\t"+"\t\t".join(str(ind) for ind in range(self.size)))
        print("\t"+"-"*(self.size*(2*7+2)+1))
        for ind, row in enumerate(self):
            print("\t%s" % ind + "|\t"+"\t|\t".join("(%s%d)" % r if s == CHECKED else "[%s%d]" % r if s == MARKED else "%s%d" % r for r, s in row)+"\t|")
            print("\t"+"-"*(self.size*(2*7+2)+1))
        # print("\n".join(map("\t|\t".join, self)))

    @logged
    def find_molecule_in_board(self, indeces):
        atoms = list()
        for x, y in indeces:
            atoms.append(self[x][y][0])
        return Molecule(atoms)

    @logged
    def mark_molecules_in_board(self, indeces, mark):
        for x, y in indeces:
            self[x][y][1] = mark
