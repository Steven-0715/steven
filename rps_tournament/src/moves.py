from __future__ import annotations
from enum import Enum


class Move(Enum):
    ROCK = "R"
    PAPER = "P"
    SCISSORS = "S"

    @staticmethod
    def from_input(text: str) -> "Move | None":
        t = text.strip().upper()
        for m in Move:
            if m.value == t:
                return m
        return None


def outcome(a: Move, b: Move) -> int:
    """
    Returns:
    1 if a wins, 0 if tie, -1 if a loses
    """
    if a == b:
        return 0
    wins = {
        Move.ROCK: Move.SCISSORS,
        Move.PAPER: Move.ROCK,
        Move.SCISSORS: Move.PAPER,
    }
    return 1 if wins[a] == b else -1
