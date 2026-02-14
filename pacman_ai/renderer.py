from __future__ import annotations

import importlib.util
import os
import time
from typing import Callable

from .game import Direction, GameState


def has_curses_support() -> bool:
    return importlib.util.find_spec("_curses") is not None and os.isatty(0) and os.isatty(1)


def key_to_direction(key: str) -> Direction:
    mapping = {
        "w": Direction.UP,
        "a": Direction.LEFT,
        "s": Direction.DOWN,
        "d": Direction.RIGHT,
        "": Direction.STAY,
    }
    return mapping.get(key.lower(), Direction.STAY)


def render_ascii(state: GameState) -> str:
    grid = [[" " for _ in range(state.width)] for _ in range(state.height)]
    for r, c in state.walls:
        grid[r][c] = "#"
    for r, c in state.food:
        grid[r][c] = "."
    for r, c in state.ghosts:
        grid[r][c] = "G"
    pr, pc = state.pacman
    grid[pr][pc] = "P"
    return "\n".join("".join(row) for row in grid)


def run_curses_game(loop_step: Callable[[int], tuple[bool, GameState]]) -> None:
    import curses

    keymap = {
        curses.KEY_UP: "UP",
        curses.KEY_DOWN: "DOWN",
        curses.KEY_LEFT: "LEFT",
        curses.KEY_RIGHT: "RIGHT",
        ord("w"): "UP",
        ord("s"): "DOWN",
        ord("a"): "LEFT",
        ord("d"): "RIGHT",
    }

    def wrapped(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(120)
        while True:
            raw_key = stdscr.getch()
            key = raw_key
            if raw_key in keymap:
                key = ord(keymap[raw_key][0].lower())
            should_exit, state = loop_step(key)
            stdscr.erase()
            stdscr.addstr(0, 0, render_ascii(state))
            stdscr.addstr(state.height + 1, 0, f"Score: {state.score}  Steps: {state.step_count}")
            stdscr.addstr(state.height + 2, 0, "Controls: arrows/WASD to move, q to quit")
            if state.is_win:
                stdscr.addstr(state.height + 3, 0, "You won! Press q to exit.")
            elif state.is_lose:
                stdscr.addstr(state.height + 3, 0, "You lost! Press q to exit.")
            stdscr.refresh()
            if should_exit:
                break
            time.sleep(0.03)

    curses.wrapper(wrapped)


def run_text_game(loop_step: Callable[[str], tuple[bool, GameState]], auto: bool = False) -> None:
    while True:
        key = ""
        if not auto:
            key = input("Move [WASD, Enter=stay, q=quit]: ").strip().lower()
        should_exit, state = loop_step(key)
        print(render_ascii(state))
        print(f"Score: {state.score}  Steps: {state.step_count}")
        if state.is_win:
            print("You won!")
        elif state.is_lose:
            print("You lost!")
        if should_exit or state.is_win or state.is_lose:
            break
        if auto:
            time.sleep(0.15)
