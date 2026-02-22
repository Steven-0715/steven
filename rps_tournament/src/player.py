from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from src.moves import Move


@dataclass
class Player:
    name: str
    is_human: bool = False

    # Basic stats for report/testing
    wins: int = 0
    losses: int = 0
    ties: int = 0
    move_counts: Dict[Move, int] = None

    def __post_init__(self) -> None:
        if self.move_counts is None:
            self.move_counts = {Move.ROCK: 0, Move.PAPER: 0, Move.SCISSORS: 0}

    def record_move(self, move: Move) -> None:
        self.move_counts[move] += 1
