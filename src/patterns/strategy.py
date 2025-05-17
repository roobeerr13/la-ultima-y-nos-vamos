import random

class TieBreakerStrategy:
    def resolve(self, options):
        return random.choice(options)

class RandomTieBreaker(TieBreakerStrategy):
    pass