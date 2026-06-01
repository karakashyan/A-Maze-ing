*This project has been created as part of the 42 curriculum by ekarakas, arptadev.*

# A-Maze-ing

A-Maze-ing is a Python maze generator and terminal visualizer. It reads a configuration file, generates a valid maze, saves it in hexadecimal wall format, finds the shortest path, and displays the result in an interactive terminal view.

## Features

- Config-based maze generation
- Reproducible output with `SEED`
- Perfect and non-perfect maze modes
- DFS-based iterative backtracking generation
- BFS shortest path search
- Hexadecimal output format
- Visible `42` pattern made from closed cells
- Interactive terminal display with `curses`
- Bonus animation for generation and animal movement
- Reusable `MazeGenerator` package: `mazegen-ekarakas-arptadev`
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
├── Makefile
├── README.md
├── pyproject.toml
└── mazegen/
    ├── __init__.py
    └── maze_generator.py
```

Generated after running:

```text
maze.txt
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

The configuration file contains one `KEY=VALUE` pair per line. Lines starting with `#` are ignored.

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

| Key | Description |
|---|---|
| `WIDTH` | Maze width in cells |
| `HEIGHT` | Maze height in cells |
| `ENTRY` | Entry coordinates in `x,y` format |
| `EXIT` | Exit coordinates in `x,y` format |
| `OUTPUT_FILE` | Name of the generated output file |
| `PERFECT` | `True` for a perfect maze, `False` for extra loops |
| `SEED` | Random seed for reproducible generation |

The config uses `x,y` coordinates. Inside the code, cells are stored as `(row, col)`, so coordinates are converted when they are loaded.

## Output file format

The maze is saved with one hexadecimal digit per cell. Each digit stores the closed walls of a cell.

| Bit | Direction |
|---|---|
| 0 | North |
| 1 | East |
| 2 | South |
| 3 | West |

After the maze rows, the file contains an empty line and then:

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

The path uses only `N`, `E`, `S`, and `W`.

## Algorithm

The maze is generated with **DFS-based iterative backtracking**.

The generator starts from one cell, chooses a random unvisited neighbour, removes the wall between the two cells, moves forward, and backtracks with a stack when no unvisited neighbours remain.

This algorithm was chosen because it is simple, reliable, reproducible with a seed, and naturally creates a perfect maze when `PERFECT=True`.

## Perfect and non-perfect mazes

When `PERFECT=True`, the maze has exactly one path between connected cells.

When `PERFECT=False`, the program first creates a perfect maze and then opens extra safe walls to add loops. The code avoids invalid `3x3` open areas, so corridors do not become too wide.

## Shortest path

The shortest valid path from entry to exit is found with **Breadth-First Search**.

BFS was chosen because all moves have equal cost, so it guarantees the shortest path in an unweighted maze.

## 42 pattern

The visual maze contains a visible `42` pattern.

The pattern:

- is placed near the centre of the maze;
- is made from fully closed cells;
- is treated as blocked cells;
- is avoided during generation and pathfinding;
- cannot overlap with entry or exit.

If the maze is too small for the pattern, the program prints a clear error message and stops gracefully.

## Visual representation

The project uses terminal rendering with Unicode characters and `curses`. The visual display shows walls, entry, exit, the shortest path, and the `42` pattern.

Interactive keys:

| Key | Action |
|---|---|
| `q` | Quit |
| `p` | Show or hide the shortest path |
| `r` | Regenerate the maze |
| `c` | Change wall colours |
| `a` | Toggle animated generation |
| `m` | Move the animal to the food bonus animation |

If the terminal does not support `curses`, the maze is still generated and saved, and the program prints a warning instead of crashing.

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

`make lint` runs `flake8` and `mypy` with the required flags. `make lint-strict` runs:

```bash
flake8 .
mypy . --strict
```

## Reusable package

The reusable part of the project is the `MazeGenerator` class. It is available in the root module and in the package directory:

```text
maze_generator.py
mazegen/maze_generator.py
```

Build the package:

```bash
python3 -m build
```

Install the generated wheel:

```bash
python3 -m pip install dist/mazegen_ekarakas_arptadev-0.1.0-py3-none-any.whl
```

Basic usage:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(width=20, height=15, seed=1, perfect=True)
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
| `generate_steps()` | Generate the maze step by step for animation |
| `add_42_pattern()` | Add the closed-cell `42` pattern |
| `find_shortest_path()` | Find the shortest path with BFS |
| `path_to_directions()` | Convert path cells to `N/E/S/W` directions |
| `save_hex()` | Save the maze in subject output format |

## Error handling

The program handles invalid input gracefully, including:

- missing config file;
- bad config syntax;
- missing required keys;
- invalid numeric or boolean values;
- entry or exit outside the maze;
- entry equal to exit;
- maze too small for the `42` pattern;
- entry or exit overlapping the `42` pattern;
- no valid path from entry to exit;
- unsupported terminal for interactive mode.

## Team and project management

### Team members and roles

- **ekarakas**: mainly worked on maze generation logic, DFS-based iterative backtracking, configuration handling, output file format, testing, and project integration.
- **arptadev**: mainly worked on shortest path search with BFS, visual representation, interactive mode, README, reusable package preparation, and final checks.

Although some parts had a main responsible person, the project was developed collaboratively. The overall architecture, maze logic, visual behaviour, debugging, testing, and final improvements were discussed and implemented together step by step.

### Planning

The project started with reading the subject and understanding the required input format, output format, maze validity rules, and visual requirements. Then the work was split into small modules: config parser, maze generator, pathfinding, renderer, interactive mode, README, and reusable package.

During development, the plan evolved as edge cases appeared, especially around the `42` pattern, non-perfect mazes, `3x3` open areas, and terminal animation. The final version was improved through repeated testing with `flake8`, `mypy`, manual runs, and peer-style review.

### What worked well

- Splitting the project into clear modules.
- Using DFS for generation and BFS for shortest path.
- Keeping output file logic separate from visual bonus features.
- Checking the project with strict linting and type checking.

### What could be improved

- Add more automated unit tests.
- Support more maze generation algorithms.
- Improve terminal compatibility for more environments.

### Tools used

- Python 3
- `random`
- `collections.deque`
- `curses`
- `flake8`
- `mypy`
- `setuptools` / `build`
- Git
- AI assistant for explanations, review, README help, and edge-case checking

## Resources and AI usage

Resources used:

- Python documentation
- `random` module documentation
- `collections.deque` documentation
- `curses` documentation
- `flake8` documentation
- `mypy` documentation
- Articles and explanations about recursive backtracking
- Articles and explanations about BFS shortest path search

AI was used as a learning and review assistant. It helped with planning, explanations, code review, edge-case checking, README preparation, and checking the project against the subject. All generated or suggested content was reviewed, understood, and tested by the team before being used.
