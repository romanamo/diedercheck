from abc import ABC
from functools import reduce
from typing import Generic, List, TypeVar

from groups import Dihedral, Group, Permutation

T = TypeVar("T")


class Check(ABC, Generic[T]):
    """Check base class
    """

    def __init__(self, permutations: List[Permutation], group: Group[T], valid: T) -> bool:
        self.permutations = permutations
        self.group = group
        self.valid = valid

    def check(self, items: List[T]) -> bool:
        """Check items.

        :param items: items to check
        :return: if items are valid
        """
        permuted = []
        for i, item in enumerate(items):
            permutation = self.permutations[i % len(self.permutations)]
            applied = permutation.apply(self.group.elements())
            retrieved = applied[self.group.elements().index(item)]

            permuted.append(retrieved)

        reduced = reduce(self.group.binary, permuted)

        return reduced == self.valid


class DeutscheMark(Check):
    """Check algorithm for the Deutsche Mark (DM).

    Checks a valid serial number of a DM serial number.
    """

    def __init__(self) -> bool:
        d5 = Dihedral(5)
        base = Permutation([1, 5, 7, 6, 2, 8, 3, 0, 9, 4])

        swaps = [base ** i for i in range(1, 11)] + [Permutation.identity(10)]

        super().__init__(swaps, d5, d5.neutral())

    def check_serial(self, serial_number: str) -> bool:
        """Checks if a serial_number is valid.

        :param word: word to check
        :return: if word is valid
        """
        if len(serial_number) != 11:
            return False

        changed = self._exchange(serial_number)
        translated = list(map(self._translate, changed))

        return self.check(translated)

    def _translate(self, i: int):
        return self.group.elements()[i]

    def _exchange(self, word: str) -> List[int]:
        change: List[str] = ["A", "D", "G", "K", "L", "N", "S", "U", "Y", "Z"]

        return [int(c) if c.isdigit() else change.index(c.upper()) for c in word]
