#!/usr/bin/env python

import random
from core.debug import logged
from core.molecule import Molecule
from collections import namedtuple

Index = namedtuple('Index', 'x y')


class BoardItemStatus:
    EMPTY, MARKED, CHECKED = range(3)


class BoardItem(object):
    def __init__(self, atom, count=1, status=BoardItemStatus.EMPTY):
        self.atom = atom
        self.count = count
        self.status = status

    def __eq__(self, other):
        return self.atom == other.atom and \
            self.count == other.count and \
            self.status == other.status

    def __repr__(self):
        return "%s(%s, %s, %s)" % \
            (self.__class__.__name__, self.atom, self.count, self.status)


class Board(tuple):
    def __new__(cls, iterable, size):
        self = tuple.__new__(cls, iterable)
        self.size = size
        return self

    def __repr__(self):
        return "<Board size=%sx%s>" % (self.size, self.size)

    @logged
    def index(self, x, y):
        return x * self.size + y

    @classmethod
    @logged
    def generate(cls, size, atoms):
        atoms = list(atoms)
        return cls(tuple(BoardItem(*random.choice(atoms))
                   for _ in range(size * size)), size)

    @logged
    def find_molecule_in_board(self, indeces):
        atoms = Molecule()
        for x, y in indeces:
            index = self.index(x, y)
            atoms[self[index].atom] += self[index].count
        return Molecule(atoms)

    @logged
    def mark_molecules_in_board(self, indeces, mark=BoardItemStatus.CHECKED):
        for x, y in indeces:
            index = self.index(x, y)
            self[index].status = mark

    @logged
    def neighbours(self, one, two):
        _neighbourhood = ((0, -1), (0, 1), (-1, 0), (1, 0))
        for nbh in _neighbourhood:
            if one[0] == two[0] + nbh[0] and one[1] == two[1] + nbh[1]:
                return True

        return False

    @logged
    def is_path(self, *indeces):
        return all(self.neighbours(one, two)
                   for one, two in zip(indeces[:-1], indeces[1:]))

    @logged
    def all_marked(self, mark=BoardItemStatus.CHECKED):
        return all(cell.status == mark for cell in self)
