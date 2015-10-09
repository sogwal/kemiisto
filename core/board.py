#!/usr/bin/env python

import random
from core.debug import logged
from core.molecule import Molecule
from collections import namedtuple

I = namedtuple('Index', 'x y')


class BoardItemStatus:
    EMPTY, MARKED, CHECKED = range(3)


class BoardItem(object):
    def __init__(self, atom, status=BoardItemStatus.EMPTY):
        self.atom = atom
        self.status = status

    def to_string(self):
        return "%s%d" % (self.atom.atom, self.atom.number) \
            if self.atom.number > 1 else "%s" % self.atom.atom

    def __eq__(self, other):
        if not other:
            return False
        return self.atom.atom == other.atom.atom and \
            self.atom.number == other.atom.number and \
            self.status == other.status

    def __repr__(self):
        return "%s(%s, %s)" % \
            (self.__class__.__name__, self.atom, self.status)

    def checked(self):
        self.status = BoardItemStatus.CHECKED

    def marked(self):
        self.status = BoardItemStatus.MARKED

    def empty(self):
        self.status = BoardItemStatus.EMPTY


class Board(tuple):
    def __new__(cls, iterable, size):
        self = tuple.__new__(cls, iterable)
        self.size = size
        return self

    def __repr__(self):
        return "<Board size=%sx%s>" % (self.size, self.size)

    @logged
    def index(self, index):
        return index.x * self.size + index.y

    @classmethod
    @logged
    def generate(cls, size, atoms):
        atoms = list(atoms)
        return cls(tuple(BoardItem(random.choice(atoms))
                   for _ in range(size * size)), size)

    @logged
    def find_molecule_in_board(self, indeces):
        return Molecule("".join(self[self.index(i)].to_string()
                                for i in indeces))

    @logged
    def mark_molecules_in_board(self, indeces, mark=BoardItemStatus.CHECKED):
        for i in indeces:
            index = self.index(i)
            self[index].status = mark

    @logged
    def neighbours(self, one, two):
        _neighbourhood = (I(0, -1), I(0, 1), I(-1, 0), I(1, 0))
        for nbh in _neighbourhood:
            if one.x == two.x + nbh.x and \
                    one.y == two.y + nbh.y:
                return True

        return False

    @logged
    def is_path(self, *indeces):
        return all(self.neighbours(one, two)
                   for one, two in zip(indeces[:-1], indeces[1:]))

    @logged
    def all_marked(self, mark=BoardItemStatus.CHECKED):
        return all(cell.status == mark for cell in self)
