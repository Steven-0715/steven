from __future__ import annotations
from dataclasses import dataclass
from src.moves import Move, outcome
from src.player import Player
from src.settings import Settings
from src.ai import BaseAI, RandomAI, CounterMostCommonAI


@dataclass
class MatchResult:
    winner: Player
    loser: Player
    rounds_played: int


class Match:
    def __init__(self, p1: Player, p2: Player, best_of: int = Settings.BEST_OF) -> None:
        self.p1 = p1
        self.p2 = p2
        self.best_of = best_of
        self.need = best_of // 2 + 1

        # AI brains (only used if player is not human)
        self.ai1: BaseAI = CounterMostCommonAI()
        self.ai2: BaseAI = RandomAI()

        self.p1_history: list[Move] = []
        self.p2_history: list[Move] = []

    def _human_pick(self, player_name: str) -> Move:
        while True:
            raw = input(f"{player_name}, pick (R/P/S): ").strip()
            m = Move.from_input(raw)
            if m is not None:
                return m
            print("Invalid. Please type R, P, or S.")

    def _pick(self, player: Player, ai: BaseAI, opponent_history: list[Move]) -> Move:
        if player.is_human:
            return self._human_pick(player.name)
        return ai.choose(opponent_history)

    def play(self) -> MatchResult:
        p1_score = 0
        p2_score = 0
        rounds = 0

        while p1_score < self.need and p2_score < self.need:
            rounds += 1

            m1 = self._pick(self.p1, self.ai1, self.p2_history)
            m2 = self._pick(self.p2, self.ai2, self.p1_history)

            self.p1.record_move(m1)
            self.p2.record_move(m2)

            self.p1_history.append(m1)
            self.p2_history.append(m2)

            res = outcome(m1, m2)
            if res == 1:
                p1_score += 1
                self.p1.wins += 1
                self.p2.losses += 1
                print(f"Round {rounds}: {self.p1.name} {m1.name} vs {self.p2.name} {m2.name} -> {self.p1.name} wins")
            elif res == -1:
                p2_score += 1
                self.p2.wins += 1
                self.p1.losses += 1
                print(f"Round {rounds}: {self.p1.name} {m1.name} vs {self.p2.name} {m2.name} -> {self.p2.name} wins")
            else:
                self.p1.ties += 1
                self.p2.ties += 1
                print(f"Round {rounds}: {self.p1.name} {m1.name} vs {self.p2.name} {m2.name} -> tie")

            print(f"Score: {self.p1.name} {p1_score} - {self.p2.name} {p2_score}\n")

        winner, loser = (self.p1, self.p2) if p1_score > p2_score else (self.p2, self.p1)
        return MatchResult(winner=winner, loser=loser, rounds_played=rounds)
