#!/usr/bin/env python

from core.molecule import Atom

H2 = Atom("H", 2)
Na = Atom("Na", 1)
Na2 = Atom("Na", 2)
Cl = Atom("Cl", 1)
O2 = Atom("O", 2)
O = Atom("O", 1)

NaCl = [Atom("Na", 1), Atom("Cl", 1)]
H2O = [Atom("H", 2), Atom("O", 1)]
H2O2 = [Atom("H", 2), Atom("O", 2)]
H2SO4 = [Atom("H", 2), Atom("S", 1), Atom("O", 4)]
