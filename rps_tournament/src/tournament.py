from __future__ import annotations
from typing import List
from src.player import Player
from src.match import Match


class Tournament:
    def __init__(self, players: List[Player], best_of: int) -> None:
        self.players = players[:]
        self.best_of = best_of

    def run(self) -> Player:
        round_num = 1
        current = self.players

        while len(current) > 1:
            print(f"\n=== TOURNAMENT ROUND {round_num} ===")
            winners: List[Player] = []

            for i in range(0, len(current), 2):
                p1 = current[i]
                p2 = current[i + 1]
                print(f"\nMatch: {p1.name} vs {p2.name} (best-of-{self.best_of})")
                match = Match(p1, p2, self.best_of)
                result = match.play()
                print(f"✅ Winner: {result.winner.name} (Rounds: {result.rounds_played})")
                winners.append(result.winner)

            current = winners
            round_num += 1

        return current[0]
