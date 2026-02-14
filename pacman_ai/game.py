from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


Position = tuple[int, int]


class Direction(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    STAY = "STAY"


DIRECTION_DELTAS: dict[Direction, tuple[int, int]] = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
    Direction.STAY: (0, 0),
}


@dataclass(slots=True)
class GameConfig:
    ghost_chase_prob: float = 0.7
    max_steps: int = 500


@dataclass(slots=True)
class GameState:
    walls: set[Position]
    food: set[Position]
    pacman: Position
    ghosts: list[Position]
    width: int
    height: int
    score: int = 0
    step_count: int = 0
    is_win: bool = False
    is_lose: bool = False
    config: GameConfig = field(default_factory=GameConfig)

    def clone(self) -> "GameState":
        return GameState(
            walls=set(self.walls),
            food=set(self.food),
            pacman=self.pacman,
            ghosts=list(self.ghosts),
            width=self.width,
            height=self.height,
            score=self.score,
            step_count=self.step_count,
            is_win=self.is_win,
            is_lose=self.is_lose,
            config=self.config,
        )

    def in_bounds(self, position: Position) -> bool:
        r, c = position
        return 0 <= r < self.height and 0 <= c < self.width

    def is_wall(self, position: Position) -> bool:
        return position in self.walls

    def legal_moves(self, position: Position) -> list[Direction]:
        moves: list[Direction] = []
        for direction in (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT):
            nxt = apply_direction(position, direction)
            if self.in_bounds(nxt) and not self.is_wall(nxt):
                moves.append(direction)
        return moves

    def move_pacman(self, direction: Direction) -> None:
        if self.is_win or self.is_lose:
            return
        if direction not in self.legal_moves(self.pacman):
            direction = Direction.STAY
        self.pacman = apply_direction(self.pacman, direction)
        self.step_count += 1
        self.score -= 1
        if self.pacman in self.food:
            self.food.remove(self.pacman)
            self.score += 10
        if self.pacman in self.ghosts:
            self.is_lose = True
        if not self.food:
            self.is_win = True
        if self.step_count >= self.config.max_steps:
            self.is_lose = True

    def move_ghosts(self) -> None:
        if self.is_win or self.is_lose:
            return
        moved: list[Position] = []
        for ghost in self.ghosts:
            direction = best_ghost_move(self, ghost)
            moved.append(apply_direction(ghost, direction))
        self.ghosts = moved
        if self.pacman in self.ghosts:
            self.is_lose = True


def apply_direction(position: Position, direction: Direction) -> Position:
    dr, dc = DIRECTION_DELTAS[direction]
    return position[0] + dr, position[1] + dc


def manhattan_distance(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def best_ghost_move(state: GameState, ghost: Position) -> Direction:
    legal = state.legal_moves(ghost)
    if not legal:
        return Direction.STAY
    legal.sort(key=lambda direction: manhattan_distance(apply_direction(ghost, direction), state.pacman))
    return legal[0]


def parse_level(level: str, config: GameConfig | None = None) -> GameState:
    lines = [line.rstrip("\n") for line in level.splitlines() if line.strip()]
    width = max(len(line) for line in lines)
    walls: set[Position] = set()
    food: set[Position] = set()
    ghosts: list[Position] = []
    pacman: Position | None = None

    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "#":
                walls.add((r, c))
            elif char == ".":
                food.add((r, c))
            elif char == "P":
                pacman = (r, c)
            elif char == "G":
                ghosts.append((r, c))

    if pacman is None:
        raise ValueError("Level must include a pacman start position 'P'.")

    return GameState(
        walls=walls,
        food=food,
        pacman=pacman,
        ghosts=ghosts,
        width=width,
        height=len(lines),
        config=config or GameConfig(),
    )


DEFAULT_LEVEL = """
###################
#P....#.......#..G#
#.##.#.#.###.#.#..#
#....#...#...#....#
#.######.#.######.#
#.................#
###.###.#####.###.#
#...#.....G...#...#
#.###.#######.###.#
#.................#
###################
"""


def load_level(name: str = "default") -> GameState:
    if name != "default":
        raise ValueError(f"Unknown level '{name}'. Only 'default' is currently bundled.")
    return parse_level(DEFAULT_LEVEL)


def successors(state: GameState, position: Position) -> Iterable[tuple[Direction, Position]]:
    for direction in state.legal_moves(position):
        yield direction, apply_direction(position, direction)
