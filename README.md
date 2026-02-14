# Pacman AI Playground (Intro to AI)

This repository contains a **teaching-focused Pacman project** for students learning core AI search algorithms.
It is inspired by Berkeley CS188 project ideas and adapted into a lightweight Python codebase students can modify quickly.

## Learning goals

Students can:

- Play Pacman manually using keyboard controls.
- Switch to algorithmic control and compare behavior.
- Implement and tune search algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Uniform Cost Search (UCS)
  - A* Search
  - Greedy Best-First Search
- Observe practical trade-offs (path quality, speed, and safety around ghosts).

## Quick start

```bash
python -m pacman_ai.main --mode manual
# Windows-friendly text mode
python -m pacman_ai.main --mode manual --renderer text
```

### Manual mode controls

- Curses mode: Arrow keys or `WASD`
- Text mode: type `w`, `a`, `s`, `d` then Enter
- `q`: quit

### Auto mode (algorithmic)

```bash
python -m pacman_ai.main --mode auto --algorithm astar --speed medium
```

Try alternatives:

```bash
python -m pacman_ai.main --mode auto --algorithm bfs
python -m pacman_ai.main --mode auto --algorithm dfs
python -m pacman_ai.main --mode auto --algorithm ucs
python -m pacman_ai.main --mode auto --algorithm greedy
```

Speed options for auto mode:

- `--speed slow`: 1 move every 2 seconds
- `--speed medium`: 1 move every 1 second
- `--speed fast`: 2 moves every 1 second

## Project structure

- `pacman_ai/game.py`
  - Game state representation and transition logic.
  - Grid parsing and default level.
- `pacman_ai/algorithms.py`
  - Search implementations and algorithm registry.
- `pacman_ai/renderer.py`
  - ASCII/curses rendering and keyboard mapping.
- `pacman_ai/main.py`
  - CLI and game loop.
- `tests/test_algorithms.py`
  - Sanity checks for search correctness.

## Assignment ideas for students

1. **Search quality comparison**
   - Record average score and steps across algorithms.
2. **Heuristic design**
   - Replace Manhattan heuristic with a safer ghost-aware heuristic.
3. **Adversarial AI extension**
   - Add minimax / expectimax for ghost-aware planning.
4. **RL extension**
   - Add Q-learning agent and compare against search agents.
5. **Level design + benchmarking**
   - Create levels that reveal strengths/weaknesses of each strategy.

## Notes

- This project is terminal-based so it runs with only Python standard library.
- On Windows (or terminals without curses), use `--renderer text` for a fully playable fallback.
- Some IDE terminals may not fully support curses rendering. Run in a standard terminal if needed.
