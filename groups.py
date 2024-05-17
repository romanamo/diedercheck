from __future__ import annotations
from typing import Tuple, List
from collections.abc import Sequence

import numpy as np

class Dieder:

    def __init__(self, n: int) -> None:
        if n < 3:
            raise ValueError("Not Supported yet")
        flip = Permutation(tuple(range(n-1,-1,-1)))

        self.schemes = {
            "actions" : [f"r{i}" for i in range(n)] + [f"s{i}" for i in range(n)],
            "numbers" : list(range(2 * n)),
            "details" : ["e"] + [f"d{i}" for i in range(n-1)] + ["s"] + [f"sd{i}" for i in range(n-1)]
        }

        self.rotations = [Permutation([(i+j) % n for j in range(n)]) for i in range(n)]
        self.flipped = [r * flip for r in self.rotations]

        self.dn = self.rotations + self.flipped

    
    def table(self, name="sr"):
        return np.array([[self.schemes[name][self.dn.index(self.dn[i] * self.dn[j])] for j in range(len(self.dn))] for i in range(len(self.dn))])

class Permutation(Sequence):

    def __init__(self, mapping: List[int]) -> None:
        self.perm = mapping
        super().__init__()

    def __len__(self) -> int:
        return len(self.perm)

    def __getitem__(self, i):
        return self.perm[i]

    def __mul__(self, other: Permutation) -> Permutation:

        if len(self) != len(other):
            raise ValueError(f"Unable to compose Permutations of different lengths {len(self)}-{len(other)}")

        return Permutation([self[other[i]] for i in range(len(self))])

    def __str__(self) -> str:
        return "P" + str(self.perm)

    def __repr__(self) -> str:
        return "P" + str(self.perm)
    
    def __eq__(self, value: object) -> bool:
        return self.perm == value.perm
