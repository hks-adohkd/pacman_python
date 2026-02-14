from __future__ import annotations

import argparse
import sys

from .algorithms import ALGORITHMS, choose_action
from .game import load_level
from .renderer import has_curses_support, key_to_direction, run_curses_game, run_text_game


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pacman AI playground for Intro to AI")
    parser.add_argument("--mode", choices=["manual", "auto"], default="manual", help="manual keyboard play or auto algorithmic control")
    parser.add_argument("--algorithm", choices=sorted(ALGORITHMS.keys()), default="astar", help="Algorithm used in auto mode")
    parser.add_argument("--max-steps", type=int, default=500)
    parser.add_argument(
        "--renderer",
        choices=["auto", "curses", "text"],
        default="auto",
        help="render backend: auto-detect, force curses, or force text",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    state = load_level()
    state.config.max_steps = args.max_steps

    def step_with_char(key: str):
        if key in ("q", "Q"):
            return True, state
        if state.is_win or state.is_lose:
            return False, state

        if args.mode == "manual":
            direction = key_to_direction(key)
        else:
            direction = choose_action(state, args.algorithm)

        before = state.pacman
        state.move_pacman(direction)
        if state.pacman != before:
            state.move_ghosts()
        return False, state

    def step_with_int(key: int):
        if args.mode == "manual" and key == -1:
            return False, state
        if key == -1:
            normalized = ""
        else:
            normalized = chr(key) if 0 <= key < 128 else ""
        return step_with_char(normalized)

    use_curses = args.renderer == "curses" or (args.renderer == "auto" and has_curses_support())

    if use_curses:
        run_curses_game(step_with_int, initial_state=state, auto=args.mode == "auto")
    else:
        print("Using text renderer (curses unavailable or disabled).")
        run_text_game(step_with_char, initial_state=state, auto=args.mode == "auto")

    return 0


if __name__ == "__main__":
    sys.exit(main())
