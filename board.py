#!/usr/bin/env python

import logging
import random
from util import logged
from molecule import Molecule
from collections import defaultdict

EMPTY = ""
MARKED = "o"
CHECKED = "X"


class Board(tuple):
    def __new__(cls, iterable, size):
        self = tuple.__new__(cls, iterable)
        self.size = size
        return self

    def __repr__(self):
        return "<Board size=%sx%s>" % (self.size, self.size)


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
        logging.debug("%s", str(self))
        print("\t\t"+"\t\t".join(str(ind) for ind in range(self.size)))
        print("\t"+"-"*(self.size*(2*7+2)+1))
        for ind, row in enumerate(self):
            print("\t%s" % ind + "|\t"+"\t|\t".join("(%s%d)" % r if s == CHECKED else "[%s%d]" % r if s == MARKED else "%s%d" % r for r, s in row)+"\t|")
            print("\t"+"-"*(self.size*(2*7+2)+1))
        # print("\n".join(map("\t|\t".join, self)))

    @logged
    def find_molecule_in_board(self, indeces):
        atoms = defaultdict(int)
        for x, y in indeces:
            atoms[self[x][y][0][0]] += self[x][y][0][1]
        return Molecule(atoms)

    @logged
    def mark_molecules_in_board(self, indeces, mark):
        for x, y in indeces:
            self[x][y][1] = mark

    @logged
    def neighbours(self, one, two):
        NEIGBOURHOOD = ((0, -1), (0, 1), (-1, 0), (1, 0))
        for nbh in NEIGBOURHOOD:
            if one[0] == two[0] + nbh[0] and one[1] == two[1] + nbh[1]:
                return True

        return False 

    @logged
    def is_path(self, *indeces):
        return all(self.neighbours(one, two) for one, two in zip(indeces[:-1], indeces[1:]))
