#!/usr/bin/env python


H2 = ("H", 2)
Na = ("Na", 1)
Na2 = ("Na", 2)
Cl = ("Cl", 1)
O2 = ("O", 2)
O = ("O", 1)

from collections import defaultdict

NaCl = defaultdict(int, [("Na", 1), ("Cl", 1)])
H2O = defaultdict(int, [("H", 2), ("O", 1)])
H2O2 = defaultdict(int, [("H", 2), ("O", 2)])
H2SO4 = defaultdict(int, [("H", 2), ("S", 1), ("O", 4)])
