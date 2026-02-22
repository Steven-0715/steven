from __future__ import annotations
from src.settings import Settings
from src.player import Player
from src.tournament import Tournament
from src.moves import Move


class Game:
    def _ask_int(self, prompt: str, valid: set[int]) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                val = int(raw)
            except ValueError:
                print("Please enter a number.")
                continue
            if val in valid:
                return val
            print(f"Invalid. Choose from {sorted(valid)}.")

    def _build_players(self, count: int, human_name: str | None) -> list[Player]:
        players: list[Player] = []
        if human_name:
            players.append(Player(human_name, is_human=True))

        # fill the rest with AI players
        ai_needed = count - len(players)
        for i in range(ai_needed):
            players.append(Player(f"AI_{i+1}", is_human=False))
        return players

    def _print_stats(self, players: list[Player]) -> None:
        print("\n=== STATS (for report/testing) ===")
        for p in players:
            mc = p.move_counts
            print(
                f"{p.name}: W={p.wins} L={p.losses} T={p.ties} | "
                f"R={mc[Move.ROCK]} P={mc[Move.PAPER]} S={mc[Move.SCISSORS]}"
            )

    def run(self) -> None:
        print("\nRock–Paper–Scissors Tournament")
        print("Goal: Win a knockout tournament bracket.")
        print(Settings.MOVES_TEXT)

        while True:
            mode = input("\nMode: (1) Watch AI tournament (2) Play as human (Q) Quit: ").strip().upper()
            if mode == "Q":
                print("Bye.")
                return
            if mode not in {"1", "2"}:
                print("Invalid.")
                continue

            player_count = self._ask_int("Players (4/8/16): ", {4, 8, 16})
            best_of = self._ask_int("Best-of per match (3/5/7): ", {3, 5, 7})

            human_name = None
            if mode == "2":
                human_name = input("Your name: ").strip() or "Player"

            players = self._build_players(player_count, human_name)
            tour = Tournament(players, best_of)
            champion = tour.run()

            print(f"\n🏆 CHAMPION: {champion.name}\n")
            self._print_stats(players)

            again = input("\nPlay again? (Y/N): ").strip().upper()
            if again != "Y":
                print("Bye.")
                return
