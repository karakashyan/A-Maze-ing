*This project has been created as part of the 42 curriculum by ekarakas, arptadev.*

# A-Maze-ing

## Description

A-Maze-ing is a Python project that generates and displays mazes.

The program reads a configuration file, generates a maze using a reproducible seed, saves the result in hexadecimal wall format, finds the shortest path from entry to exit, and displays the maze in an interactive terminal view.

## Features

- Python 3.10+
- Configuration file parser
- Seed-based maze generation
- Perfect maze support
- Non-perfect maze support with extra loops
- Hexadecimal output file
- Shortest path using BFS
- Unicode terminal rendering
- Interactive controls with `curses`
- Visible `42` pattern made from fully closed cells
- Animation bonus during maze generation
- `flake8` and `mypy` support

## Project structure

```text
A-Maze-ing/
├── a_maze_ing.py
├── config.txt
├── config_parser.py
├── interactive.py
├── maze_generator.py
├── renderer.py
├── maze.txt
├── Makefile
└── README.md
```

## Usage

Run the project with:

```bash
python3 a_maze_ing.py config.txt
```

Or with Makefile:

```bash
make run
```

## Configuration file

Example:

```text
WIDTH=17
HEIGHT=15
ENTRY=0,0
EXIT=12,5
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=1
```

### Keys

| Key | Description |
|---|---|
| `WIDTH` | Maze width in cells |
| `HEIGHT` | Maze height in cells |
| `ENTRY` | Entry coordinates in `x,y` format |
| `EXIT` | Exit coordinates in `x,y` format |
| `OUTPUT_FILE` | Output file name |
| `PERFECT` | `True` for a perfect maze, `False` for extra loops |
| `SEED` | Random seed for reproducible generation |

Coordinates in the config file use:

```text
x,y
```

Inside the code, cells are stored as:

```text
(row, col)
```

## Output file format

The maze is saved using one hexadecimal digit per cell.

Wall bits:

| Bit | Direction |
|---|---|
| 0 | North |
| 1 | East |
| 2 | South |
| 3 | West |

After the maze grid, the file contains:

```text
entry
exit
shortest_path
```

Example:

```text
BD539153955555153
A93C6A96A915396BA

0,0
12,5
SSENESEESSSWNW
```

The shortest path is written using:

```text
N E S W
```

## Algorithm

The main algorithm is iterative recursive backtracking.

Steps:

1. Start from one cell.
2. Choose a random unvisited neighbour.
3. Remove the wall between the current cell and the neighbour.
4. Move to the neighbour.
5. If there are no unvisited neighbours, backtrack.
6. Continue until the maze is generated.

This algorithm was chosen because it is simple, reliable, easy to explain, and naturally creates perfect mazes.

## Perfect and non-perfect mode

When:

```text
PERFECT=True
```

The maze is perfect, meaning there is exactly one path between connected cells.

When:

```text
PERFECT=False
```

The program first creates a perfect maze, then opens extra safe walls to add loops. The code avoids creating invalid `3x3` open areas.

## 42 pattern

The maze contains a visible `42` pattern.

The pattern:

- is placed near the centre;
- is made from fully closed cells;
- is treated as blocked cells;
- is avoided by the generator and BFS;
- cannot overlap with entry or exit.

If the maze is too small for the pattern, the program prints an error and stops.

## Shortest path

The shortest path is found with Breadth-First Search.

BFS was chosen because it guarantees the shortest path in an unweighted grid.

## Visual representation

The project uses terminal rendering with Unicode characters and `curses`.

Interactive keys:

| Key | Action |
|---|---|
| `q` | Quit |
| `p` | Show or hide the path |
| `r` | Regenerate the maze |
| `c` | Change wall colour |
| `a` | Toggle animated generation |

## Makefile

Available rules:

```bash
make install
make run
make debug
make clean
make lint
make lint-strict
```

`make lint` runs `flake8` and `mypy` with the required flags.

`make lint-strict` runs:

```bash
flake8 .
mypy . --strict
```

## Reusable MazeGenerator

The reusable part of the project is the `MazeGenerator` class in `maze_generator.py`.

Example:

```python
from maze_generator import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    seed=1,
    perfect=True,
)

generator.generate()

entry = (0, 0)
exit_cell = (5, 12)

generator.add_42_pattern(entry, exit_cell)
path = generator.find_shortest_path(entry, exit_cell)
directions = generator.path_to_directions(path)

generator.save_hex("maze.txt", entry, exit_cell, directions)
```

Important methods:

| Method | Purpose |
|---|---|
| `generate()` | Generate the maze |
| `generate_steps()` | Generate step by step for animation |
| `add_42_pattern()` | Add the `42` pattern |
| `find_shortest_path()` | Find shortest path |
| `path_to_directions()` | Convert path to `N/E/S/W` |
| `save_hex()` | Save maze to output file |

## Error handling

The program handles:

- missing config file;
- invalid config syntax;
- invalid boolean values;
- invalid entry or exit;
- entry equal to exit;
- maze too small for the `42` pattern;
- entry or exit overlapping the `42` pattern;
- no valid path from entry to exit.

## Resources and AI usage

Resources used:

- Python documentation
- `random` module documentation
- `collections.deque` documentation
- `curses` documentation
- flake8 documentation
- mypy documentation
- Articles about recursive backtracking
- Articles about BFS shortest path

AI was used as a learning and review assistant. It helped with planning, explanations, code review, edge cases, README preparation, and checking the project against the subject. All code was reviewed and tested by the team.
