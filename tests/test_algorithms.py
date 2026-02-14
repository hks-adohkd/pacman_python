from pacman_ai.algorithms import ALGORITHMS
from pacman_ai.game import Direction, parse_level


SIMPLE_LEVEL = """
#####
#P..#
#...#
#..G#
#####
"""


def test_algorithms_move_toward_food():
    state = parse_level(SIMPLE_LEVEL)
    expected = {Direction.RIGHT, Direction.DOWN}

    for name, solver in ALGORITHMS.items():
        state_copy = state.clone()
        target = min(state_copy.food)
        path = solver(state_copy, state_copy.pacman, target)
        assert path, f"{name} returned empty path"
        assert path[0] in expected, f"{name} made unexpected first move {path[0]}"


def test_pacman_collects_food_and_scores():
    state = parse_level(SIMPLE_LEVEL)
    before_food = len(state.food)
    state.move_pacman(Direction.RIGHT)
    assert len(state.food) == before_food - 1
    assert state.score == 9
