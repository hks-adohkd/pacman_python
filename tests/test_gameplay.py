from pacman_ai.game import Direction, parse_level


LEVEL = """
#####
#PG.#
#####
"""


OPEN_LEVEL = """
######
#P.G.#
######
"""


def test_ghost_does_not_move_when_pacman_does_not_move():
    state = parse_level(LEVEL)
    pacman_before = state.pacman
    ghosts_before = list(state.ghosts)

    state.move_pacman(Direction.LEFT)  # wall, pacman stays
    if state.pacman != pacman_before:
        state.move_ghosts()

    assert state.pacman == pacman_before
    assert state.ghosts == ghosts_before


def test_ghost_moves_when_pacman_moves():
    state = parse_level(OPEN_LEVEL)
    ghosts_before = list(state.ghosts)
    pacman_before = state.pacman

    state.move_pacman(Direction.RIGHT)
    if state.pacman != pacman_before:
        state.move_ghosts()

    assert state.ghosts != ghosts_before
