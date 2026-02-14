from pacman_ai.game import Direction
from pacman_ai.renderer import direction_token_to_input, key_to_direction


def test_key_to_direction_mapping():
    assert key_to_direction("w") == Direction.UP
    assert key_to_direction("a") == Direction.LEFT
    assert key_to_direction("s") == Direction.DOWN
    assert key_to_direction("d") == Direction.RIGHT
    assert key_to_direction("") == Direction.STAY
    assert key_to_direction("x") == Direction.STAY


def test_direction_token_to_input_mapping():
    assert direction_token_to_input("UP") == "w"
    assert direction_token_to_input("DOWN") == "s"
    assert direction_token_to_input("LEFT") == "a"
    assert direction_token_to_input("RIGHT") == "d"
