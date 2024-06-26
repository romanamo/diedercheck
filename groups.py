from __future__ import annotations
from typing import List, Generic, TypeVar
from abc import ABC, abstractmethod
from collections.abc import Sequence
from functools import reduce

T = TypeVar("T")
class Group(Generic[T], ABC):

    @abstractmethod
    def binary(self, a : T, b : T) -> T:
        pass

    def neutral(self) -> T:
        pass

    def inverse(self, a : T) -> T:
        pass

    def elements(self) -> List[T]:
        pass

    def table(self) -> List[List[T]]:
        pass

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
    
    def apply(self, values):
        """Applies a permutation on a list.

        :param values: applied list of values
        :return: permuted list
        """
        return [values[self.perm[i]] for i in range(len(values))]
    
    def inverse(self) -> Permutation:
        """Get the inverse of a permutation

        :return: inverse
        """
        return Permutation([self.index(i) for i in range(len(self))])

class Dihedral(Group[Permutation]):
    """Dihedral group

    The Dihedral group D_n represents the group of symmetries 
    of a regular n-sided polygon. 
    """

    def __init__(self, n: int) -> None:
        self.n = n
        if n < 3:
            raise ValueError("Not Supported yet")
        
        self.schemes = {
            "actions": [f"r{i}" for i in range(n)] + [f"s{i}" for i in range(n)],
            "numbers": list(range(2 * n)),
            "details": ["e"] + [f"d{i}" for i in range(n-1)] + ["s"] + [f"sd{i}" for i in range(n-1)]
        }

    def neutral(self) -> Permutation:
        return Permutation.identity(self.n)
    
    def inverse(self, a: Permutation) -> Permutation:
        return a.inverse()
    
    def binary(self, a: Permutation, b: Permutation) -> Permutation:
        return a * b

    def table(self, naming: str = "details") -> List[List[str | int]]:
        """Generates a cayley table.

        Generates a cayley table using specified naming schemes:

        `"actions"`: specifies group elements by different rotations or symmetries
        `"numbers"`: specifies group elements by numbers
        `"details"`: specifies group elements by generating elements

        :param naming: naming scheme, defaults to "details"
        :return: cayley table
        """
        items = self.elements()

        return [
            [self.schemes[naming][items.index(items[i] * items[j])] for j in range(len(items))] for i in range(len(items))]
    
    def elements(self) -> List[T]:
        flip = Permutation(list(range(self.n-1, -1, -1)))
        rotations = [Permutation([(i+j) % self.n for j in range(self.n)]) for i in range(self.n)]
        
        flipped = [r * flip for r in rotations]

        return rotations + flipped
