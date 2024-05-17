from abc import ABC, abstractmethod
from typing import List
from functools import reduce

from groups import Dieder

class Check(ABC):

    @abstractmethod
    def check(self, word: str) -> bool:
        pass

class DeutscheMark(Check):

    def check(self, word: str) -> bool:
        if len(word) != 11:
            return False
        
        dieder5 = Dieder(5)
    
        changed = DeutscheMark.exchange(word)
        permuted = DeutscheMark.permute(changed)
        reduced = reduce(lambda a, b : dieder5.dn.index(dieder5.dn[a] * dieder5.dn[b]), permuted)

        return reduced == 0

    
    def exchange(word : str) -> List[int]:
        change : List[str]= ["A", "D", "G", "K", "L", "N", "S", "U", "Y", "Z"]

        return [int(c) if c.isdigit() else change.index(c.upper()) for c in word]

    def permute(digits : List[int]) -> List[int]:
        swap = [
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ]
        
        return [swap[i][digits[i]] for i in range(11)]
    
