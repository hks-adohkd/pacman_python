from pacman_ai.main import SPEED_TO_INTERVAL


def test_speed_to_interval_values():
    assert SPEED_TO_INTERVAL["slow"] == 2.0
    assert SPEED_TO_INTERVAL["medium"] == 1.0
    assert SPEED_TO_INTERVAL["fast"] == 0.5
