from __future__ import annotations

import curses
import time

from .game import GameState


KEYMAP = {
    curses.KEY_UP: "UP",
    curses.KEY_DOWN: "DOWN",
    curses.KEY_LEFT: "LEFT",
    curses.KEY_RIGHT: "RIGHT",
    ord("w"): "UP",
    ord("s"): "DOWN",
    ord("a"): "LEFT",
    ord("d"): "RIGHT",
}


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


def run_curses_game(loop_step):
    def wrapped(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(120)
        while True:
            key = stdscr.getch()
            should_exit, state = loop_step(key)
            stdscr.erase()
            stdscr.addstr(0, 0, render_ascii(state))
            stdscr.addstr(state.height + 1, 0, f"Score: {state.score}  Steps: {state.step_count}")
            if state.is_win:
                stdscr.addstr(state.height + 2, 0, "You won! Press q to exit.")
            elif state.is_lose:
                stdscr.addstr(state.height + 2, 0, "You lost! Press q to exit.")
            stdscr.refresh()
            if should_exit:
                break
            time.sleep(0.03)

    curses.wrapper(wrapped)
