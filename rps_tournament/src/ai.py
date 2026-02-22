from __future__ import annotations
import random
from typing import Dict
from src.moves import Move


class BaseAI:
    def choose(self, opponent_history: list[Move]) -> Move:
        raise NotImplementedError


class RandomAI(BaseAI):
    def choose(self, opponent_history: list[Move]) -> Move:
        return random.choice([Move.ROCK, Move.PAPER, Move.SCISSORS])


class CounterMostCommonAI(BaseAI):
    """
    Simple "algorithm" bonus:
    - Track opponent move history
    - Find the most common move
    - Play the counter move
    """
    def choose(self, opponent_history: list[Move]) -> Move:
        if not opponent_history:
            return random.choice([Move.ROCK, Move.PAPER, Move.SCISSORS])

        counts: Dict[Move, int] = {Move.ROCK: 0, Move.PAPER: 0, Move.SCISSORS: 0}
        for m in opponent_history:
            counts[m] += 1

        most_common = max(counts, key=counts.get)

        # counter move
        counter = {
            Move.ROCK: Move.PAPER,
            Move.PAPER: Move.SCISSORS,
            Move.SCISSORS: Move.ROCK,
        }
        # small randomness to avoid being too predictable
        if random.random() < 0.15:
            return random.choice([Move.ROCK, Move.PAPER, Move.SCISSORS])
        return counter[most_common]
