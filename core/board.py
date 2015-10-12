#!/usr/bin/env python

import random
import logging
from core.debug import logged
from core.molecule import Molecule
from collections import namedtuple

I = namedtuple('Index', 'x y')


class BoardItemStatus:
    EMPTY, MARKED, CHECKED = range(3)


class BoardItem(object):
    def __init__(self, atom, index, status=BoardItemStatus.EMPTY, **kwargs):
        self.atom = atom
        self.status = status
        self.index = index

    def _to_molecule_string(self):
        return "%s%d" % (self.atom.atom, self.atom.number) \
            if self.atom.number > 1 else "%s" % self.atom.atom

    def __eq__(self, other):
        if not other:
            return False
        return self.atom.atom == other.atom.atom and \
            self.atom.number == other.atom.number and \
            self.status == other.status

    def __repr__(self):
        return "%s(%s, %s, %s)" % \
            (self.__class__.__name__, self.atom, self.index, self.status)

    def checked(self):
        self.status = BoardItemStatus.CHECKED

    def marked(self):
        self.status = BoardItemStatus.MARKED

    def empty(self):
        self.status = BoardItemStatus.EMPTY


class Board(object):
    def __init__(self, iterable, length):
        self.iterable = iterable
        self.length = length

    def __repr__(self):
        return "<Board length=%sx%s>" % (self.length, self.length)

    @logged
    def index(self, index):
        return index.x * self.length + index.y

    @logged
    def generate(self, length, atoms):
        self.length = length
        self.iterable = list(self.generate_one(atoms, I(x, y))
                             for x in range(length) for y in range(length))

    @logged
    def generate_one(self, atoms, index):
        return BoardItem(random.choice(atoms), index)

    @logged
    def find_molecule_in_board(self, indeces):
        return Molecule("".join(self.iterable[self.index(i)].
                                _to_molecule_string()
                                for i in indeces))

    @logged
    def mark_molecules_in_board(self, indeces, mark=BoardItemStatus.CHECKED):
        for i in indeces:
            index = self.index(i)
            self.iterable[index].status = mark

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
        return all(cell.status == mark for cell in self.iterable)

    @logged
    def compact(self):
        new_board = [None] * self.length ** 2
        nix = 0
        for ix in range(self.length):
            none = [None] * self.length
            niy = 0
            index = self.index(I(ix, 0))
            for iy in range(self.length):
                i = I(ix, iy)
                index = self.index(i)
                item = self.iterable[index]
                if item is None:
                    continue
                if niy != iy or nix != ix:
                    item.index = I(nix, niy)
                none[niy] = item
                niy += 1
            index = self.index(I(nix, 0))
            new_board[index:index + self.length] = none
            if any(none):
                nix += 1
        self.iterable = new_board

    @logged
    def shuffle(self, times):
        indeces = [index for index, item in enumerate(self.iterable) if item]
        logging.debug("taken positions: %s", indeces)
        for _ in range(times):
            first = random.choice(indeces)
            second = random.choice(indeces)
            logging.debug("swapping %d <=> %d", first, second)
            # swap
            self.iterable[first], self.iterable[second] = \
                self.iterable[second], self.iterable[first]
            self.iterable[first].index, self.iterable[second].index = \
                self.iterable[second].index, self.iterable[first].index
