from __future__ import annotations

import heapq
from collections import deque

from .game import Direction, GameState, Position, manhattan_distance, successors


def reconstruct_path(came_from: dict[Position, tuple[Position, Direction]], goal: Position, start: Position) -> list[Direction]:
    path: list[Direction] = []
    current = goal
    while current != start:
        prev, direction = came_from[current]
        path.append(direction)
        current = prev
    path.reverse()
    return path


def nearest_food(state: GameState) -> Position | None:
    if not state.food:
        return None
    return min(state.food, key=lambda pos: manhattan_distance(state.pacman, pos))


def bfs_to_target(state: GameState, start: Position, target: Position) -> list[Direction]:
    frontier = deque([start])
    visited = {start}
    came_from: dict[Position, tuple[Position, Direction]] = {}

    while frontier:
        current = frontier.popleft()
        if current == target:
            return reconstruct_path(came_from, target, start)
        for direction, nxt in successors(state, current):
            if nxt in visited:
                continue
            visited.add(nxt)
            came_from[nxt] = (current, direction)
            frontier.append(nxt)
    return []


def dfs_to_target(state: GameState, start: Position, target: Position) -> list[Direction]:
    stack = [start]
    visited = {start}
    came_from: dict[Position, tuple[Position, Direction]] = {}

    while stack:
        current = stack.pop()
        if current == target:
            return reconstruct_path(came_from, target, start)
        for direction, nxt in successors(state, current):
            if nxt in visited:
                continue
            visited.add(nxt)
            came_from[nxt] = (current, direction)
            stack.append(nxt)
    return []


def ucs_to_target(state: GameState, start: Position, target: Position) -> list[Direction]:
    frontier: list[tuple[int, Position]] = [(0, start)]
    came_from: dict[Position, tuple[Position, Direction]] = {}
    cost = {start: 0}

    while frontier:
        g, current = heapq.heappop(frontier)
        if current == target:
            return reconstruct_path(came_from, target, start)
        if g > cost[current]:
            continue
        for direction, nxt in successors(state, current):
            new_g = g + 1
            if new_g < cost.get(nxt, float("inf")):
                cost[nxt] = new_g
                came_from[nxt] = (current, direction)
                heapq.heappush(frontier, (new_g, nxt))
    return []


def astar_to_target(state: GameState, start: Position, target: Position) -> list[Direction]:
    frontier: list[tuple[int, int, Position]] = [(manhattan_distance(start, target), 0, start)]
    came_from: dict[Position, tuple[Position, Direction]] = {}
    cost = {start: 0}

    while frontier:
        _, g, current = heapq.heappop(frontier)
        if current == target:
            return reconstruct_path(came_from, target, start)
        if g > cost[current]:
            continue
        for direction, nxt in successors(state, current):
            new_g = g + 1
            if new_g < cost.get(nxt, float("inf")):
                cost[nxt] = new_g
                came_from[nxt] = (current, direction)
                h = manhattan_distance(nxt, target)
                heapq.heappush(frontier, (new_g + h, new_g, nxt))
                came_from[nxt] = (current, direction)
    return []


def greedy_best_first_to_target(state: GameState, start: Position, target: Position) -> list[Direction]:
    frontier: list[tuple[int, Position]] = [(manhattan_distance(start, target), start)]
    visited = {start}
    came_from: dict[Position, tuple[Position, Direction]] = {}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == target:
            return reconstruct_path(came_from, target, start)
        for direction, nxt in successors(state, current):
            if nxt in visited:
                continue
            visited.add(nxt)
            came_from[nxt] = (current, direction)
            heapq.heappush(frontier, (manhattan_distance(nxt, target), nxt))
    return []


ALGORITHMS = {
    "bfs": bfs_to_target,
    "dfs": dfs_to_target,
    "ucs": ucs_to_target,
    "astar": astar_to_target,
    "greedy": greedy_best_first_to_target,
}


def choose_action(state: GameState, algorithm: str) -> Direction:
    target = nearest_food(state)
    if target is None:
        return Direction.STAY
    solver = ALGORITHMS[algorithm]
    path = solver(state, state.pacman, target)
    if not path:
        return Direction.STAY
    return path[0]
