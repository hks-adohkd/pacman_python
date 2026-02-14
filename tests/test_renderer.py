from pacman_ai.game import Direction
from pacman_ai.renderer import key_to_direction


def test_key_to_direction_mapping():
    assert key_to_direction("w") == Direction.UP
    assert key_to_direction("a") == Direction.LEFT
    assert key_to_direction("s") == Direction.DOWN
    assert key_to_direction("d") == Direction.RIGHT
    assert key_to_direction("") == Direction.STAY
    assert key_to_direction("x") == Direction.STAY
