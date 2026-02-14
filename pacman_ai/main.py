from __future__ import annotations

import argparse
import curses
import sys

from .algorithms import ALGORITHMS, choose_action
from .game import Direction, load_level
from .renderer import KEYMAP, run_curses_game


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pacman AI playground for Intro to AI")
    parser.add_argument("--mode", choices=["manual", "auto"], default="manual", help="manual keyboard play or auto algorithmic control")
    parser.add_argument("--algorithm", choices=sorted(ALGORITHMS.keys()), default="astar", help="Algorithm used in auto mode")
    parser.add_argument("--max-steps", type=int, default=500)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    state = load_level()
    state.config.max_steps = args.max_steps

    def game_step(key: int):
        if key in (ord("q"), ord("Q")):
            return True, state
        if state.is_win or state.is_lose:
            return False, state

        if args.mode == "manual":
            direction_name = KEYMAP.get(key, "STAY")
            direction = Direction(direction_name)
        else:
            direction = choose_action(state, args.algorithm)

        state.move_pacman(direction)
        state.move_ghosts()
        return False, state

    try:
        run_curses_game(game_step)
    except curses.error:  # type: ignore[name-defined]
        print("Your terminal does not support curses rendering in this environment.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
