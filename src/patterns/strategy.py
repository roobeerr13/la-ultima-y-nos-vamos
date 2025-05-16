from abc import ABC, abstractmethod
from typing import List
import random

class TieBreakerStrategy(ABC):
    @abstractmethod
    def resolve(self, options: List[str]) -> str:
        pass

class RandomTieBreaker(TieBreakerStrategy):
    def resolve(self, options: List[str]) -> str:
        return random.choice(options)

class AlphabeticalTieBreaker(TieBreakerStrategy):
    def resolve(self, options: List[str]) -> str:
        return min(options)