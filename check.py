from abc import ABC, abstractmethod
from typing import List
from functools import reduce

from dihedral import Dihedral, Permutation


class Check(ABC):
    """Check base class
    """

    @abstractmethod
    def check(self, word: str) -> bool:
        """Checks if a word is valid.

        :param word: word to check
        :return: if word is valid
        """


class DeutscheMark(Check):
    """Check algorithm for the Deutsche Mark (DM).

    Checks a valid serial number of a DM serial number.
    """

    def check(self, word: str) -> bool:
        if len(word) != 11:
            return False

        dihedral = Dihedral(5)

        changed = self._exchange(word)
        permuted = self._permute(changed)

        reduced = reduce(lambda a, b: dihedral.elements.index(
            dihedral.elements[a] * dihedral.elements[b]), permuted)

        return reduced == 0

    def _exchange(self, word: str) -> List[int]:
        change: List[str] = ["A", "D", "G", "K", "L", "N", "S", "U", "Y", "Z"]

        return [int(c) if c.isdigit() else change.index(c.upper()) for c in word]

    def _permute(self, digits: List[int]) -> List[int]:
        base = Permutation([1, 5, 7, 6, 2, 8, 3, 0, 9, 4])

        swap = [base ** i for i in range(1, 11)] + [Permutation.identity(10)]

        return [swap[i][digits[i]] for i in range(11)]
