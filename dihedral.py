from __future__ import annotations
from typing import List
from collections.abc import Sequence
from functools import reduce


class Dihedral:
    """Dihedral group

    The Dihedral group D_n represents the group of symmetries 
    of a regular n-sided polygon. 
    """

    def __init__(self, n: int) -> None:
        if n < 3:
            raise ValueError("Not Supported yet")
        flip = Permutation(list(range(n-1, -1, -1)))

        self.schemes = {
            "actions": [f"r{i}" for i in range(n)] + [f"s{i}" for i in range(n)],
            "numbers": list(range(2 * n)),
            "details": ["e"] + [f"d{i}" for i in range(n-1)] + ["s"] + [f"sd{i}" for i in range(n-1)]
        }

        self.rotations = [Permutation(
            [(i+j) % n for j in range(n)]) for i in range(n)]
        self.flipped = [r * flip for r in self.rotations]

        self.elements = self.rotations + self.flipped

    def table(self, naming: str = "details") -> List[List[str | int]]:
        """Generates a cayley table.

        Generates a cayley table using specified naming schemes:

        `"actions"`: specifies group elements by different rotations or symmetries
        `"numbers"`: specifies group elements by numbers
        `"details"`: specifies group elements by generating elements

        :param naming: naming scheme, defaults to "details"
        :return: cayley table
        """
        return [
            [self.schemes[naming][self.elements.index(self.elements[i] * self.elements[j])]
                for j in range(len(self.elements))]
            for i in range(len(self.elements))]


class Permutation(Sequence):
    """Permutation

    Represents a permutation as one dimensional array, using indices as preimage.
    """
    @staticmethod
    def identity(n: int):
        """Identity permutation of length n.

        :param n: length
        :return: identity permutation
        """
        return Permutation(list(range(n)))

    def __init__(self, mapping: List[int]) -> None:
        self.perm = mapping
        super().__init__()

    def __len__(self) -> int:
        return len(self.perm)

    def __getitem__(self, i):
        return self.perm[i]

    def __mul__(self, other: Permutation) -> Permutation:

        if len(self) != len(other):
            raise ValueError(f"Unable to compose Permutations of different lengths: {len(self)}-{len(other)}")

        return Permutation([self[other[i]] for i in range(len(self))])

    def __pow__(self, n: int):
        return reduce(lambda a, b: a * b, [self for _ in range(n)])

    def __str__(self) -> str:
        return "P" + str(self.perm)

    def __repr__(self) -> str:
        return "P" + str(self.perm)

    def __eq__(self, value: Permutation) -> bool:
        return self.perm == value.perm
    
    def inverse(self) -> Permutation:
        """Get the inverse of a permutation

        :return: inverse
        """
        return Permutation([self.index(i) for i in range(len(self))])
