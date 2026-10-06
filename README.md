*This project has been created as part of the 42 curriculum by ekarakas, arptadev.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python. It reads a configuration
file, generates a random but reproducible maze, writes it to a file using a
hexadecimal wall encoding, and displays it in the terminal with an interactive
menu.

The program supports two modes:

- **Perfect maze** (`PERFECT=True`): exactly one path between any two cells,
  no loops at all.
- **Pac-Man board** (`PERFECT=False`, the default): a fully connected board
  with several independent routes, open corners and centre, and no real
  dead-ends, so it can be reused directly as a Pac-Man-like level.

Every maze large enough contains a visible "42" drawn with fully closed cells.

The generation logic lives in a standalone, pip-installable package called
`mazegen`, so it can be reused in future projects.

## Instructions

### Requirements

- Python 3.10 or later
- A terminal with Unicode and colour support

### Installation

It is recommended to use a virtual environment, created outside of the project
folder. On machines without the `python3-venv` package, use `virtualenv`
(it needs no administrator rights):

```bash
python3 -m pip install --user virtualenv
python3 -m virtualenv ~/venvs/amazeing
source ~/venvs/amazeing/bin/activate
make install
```

### Running

```bash
python3 a_maze_ing.py config.txt
```

or simply:

```bash
make run
```

### Makefile rules

| Rule               | Description                                         |
|--------------------|-----------------------------------------------------|
| `make install`     | Install `flake8`, `mypy`, `build`, `virtualenv`     |
| `make run`         | Run the program with `config.txt`                   |
| `make debug`       | Run the program inside the `pdb` debugger           |
| `make clean`       | Remove caches and build folders (`build`, `dist`)   |
| `make lint`        | Run `flake8` and `mypy` with the mandatory flags    |
| `make lint-strict` | Run `flake8` and `mypy --strict`                    |

### Interactive controls

| Key | Action                                          |
|-----|-------------------------------------------------|
| `r` | Re-generate a new maze                          |
| `p` | Show / hide the shortest path from entry to exit |
| `c` | Rotate the wall colours                         |
| `a` | Toggle animated generation and re-generate      |
| `m` | Move the cat 🐱 along the path to the fish 🐟    |
| `q` | Quit                                            |

The "42" pattern is drawn with its own colour.

## Configuration file

The configuration file contains one `KEY=VALUE` pair per line. Lines starting
with `#` and empty lines are ignored. Spaces around `=` are allowed.

| Key           | Required | Description                         | Example             |
|---------------|----------|-------------------------------------|---------------------|
| `WIDTH`       | yes      | Maze width, from 1 to 500 cells     | `WIDTH=18`          |
| `HEIGHT`      | yes      | Maze height, from 1 to 500 cells    | `HEIGHT=15`         |
| `ENTRY`       | yes      | Entry coordinates `x,y`             | `ENTRY=2,0`         |
| `EXIT`        | yes      | Exit coordinates `x,y`              | `EXIT=15,7`         |
| `OUTPUT_FILE` | yes      | Output file name                    | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | yes      | `True` or `False`                   | `PERFECT=False`     |
| `SEED`        | no       | Random seed (default `0`)           | `SEED=1`            |

Example (`config.txt`, the default configuration of the repository):

```
WIDTH=18
HEIGHT=15
ENTRY=2,0
EXIT=15,7
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=1
```

The same seed with the same configuration always produces the same maze.

### Error handling

The program never crashes on bad input. It prints a clear message and stops
when:

- the configuration file does not exist or cannot be read;
- a line has no `=`, a key is missing, or a value is invalid
  (non-numeric size, wrong coordinates, `PERFECT` not `True`/`False`);
  the message names the wrong key, e.g. `WIDTH must be an integer, got 'abc'`;
- `WIDTH` or `HEIGHT` is not between 1 and 500 (larger mazes would not fit
  in memory);
- entry and exit are equal or outside the maze;
- entry or exit is placed on a "42" cell;
- `PERFECT=False` is impossible for the requested size (a Pac-Man board needs
  at least 2 independent loops, e.g. a 2x2 maze cannot have them);
- the output file cannot be written.

If the maze is smaller than **9x7**, the "42" pattern is omitted, an error
message is printed, and the maze is still generated.

## Output file format

Each cell is written as one hexadecimal digit. Each bit is a wall, `1` means
closed and `0` means open:

| Bit     | Direction |
|---------|-----------|
| 0 (LSB) | North     |
| 1       | East      |
| 2       | South     |
| 3       | West      |

Cells are written row by row, one row per line. After an empty line, the file
contains the entry coordinates, the exit coordinates and the shortest path from
entry to exit using the letters `N`, `E`, `S`, `W`.

The output can be checked with the provided analyzer:

```bash
python3 maze_analyzer.py maze.txt
python3 maze_analyzer.py maze.txt --max-dead-ends 0
```

## Maze generation algorithm

### Chosen algorithm: iterative recursive backtracker (randomized DFS)

1. Every cell starts with its four walls closed. The cells of the "42" pattern
   are excluded from the generation.
2. Start from cell `(0, 0)` and push it on a stack.
3. Look at the cell on top of the stack. If it has unvisited neighbours, pick
   one at random, remove the wall between them, mark it visited and push it.
4. Otherwise, pop the stack (backtrack).
5. Stop when the stack is empty: every cell has been visited.

The result is a **spanning tree** of the grid: a perfect maze.

### Pac-Man mode: braiding

When `PERFECT=False`, the perfect maze is post-processed with **braiding**:
for every dead-end (a cell with exactly one opening), one extra wall is opened
towards a random neighbour. Walls are never opened towards the outer border or
a "42" cell, and an opening is skipped if it would create a forbidden 3x3 open
area. Every removed dead-end creates a new loop, so the board becomes fully
braided: corners and centre are open corridors, there are many independent
routes, and no real dead-end remains.

### Shortest path

The shortest path from entry to exit is found with a **breadth-first search
(BFS)**, which guarantees the shortest route in an unweighted grid.

### Why this algorithm

- It is simple to understand, implement and explain.
- The iterative version uses an explicit stack, so there is no recursion limit,
  even for large mazes.
- It produces long, winding corridors that look like a real maze.
- It visits every cell, so full connectivity is guaranteed by construction.
- Braiding can only open walls, never close them, so connectivity is kept and
  one generator serves both modes: `PERFECT=True` is DFS, `PERFECT=False` is
  DFS + braiding.

## Reusable module: `mazegen`

The whole generation logic is the `MazeGenerator` class inside the `mazegen`
package. It does not depend on the rest of the project (no display, no config
file) and can be installed with pip. The package has its own documentation,
`mazegen/README.md`, which is included in the `.whl` file; the summary below
is the same.

### Installation

```bash
pip install mazegen-0.1.0-py3-none-any.whl
```

### Basic example

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
gen.generate()

entry = (0, 0)       # (row, col)
exit_cell = (14, 19) # (row, col)
gen.add_42_pattern(entry, exit_cell)

path = gen.find_shortest_path(entry, exit_cell)
print(gen.path_to_directions(path))   # e.g. "SSEEN..."
```

### Custom parameters

| Parameter | Type   | Description                                    |
|-----------|--------|------------------------------------------------|
| `width`   | `int`  | Number of columns                              |
| `height`  | `int`  | Number of rows                                 |
| `seed`    | `int`  | Random seed, same seed gives the same maze     |
| `perfect` | `bool` | `True` = perfect maze, `False` = Pac-Man board |

Note: the module uses `(row, col)` coordinates, while the configuration file
uses `(x, y)`, so `x = col` and `y = row`.

### Accessing the generated structure

- `gen.grid[row][col]` is a dictionary of walls, for example
  `{"N": True, "E": False, "S": True, "W": True}`. `True` means the wall is
  closed.
- `gen.maze_to_hex_lines()` returns the maze in the hexadecimal format.
- `gen.get_42_cells()` returns the cells of the "42" pattern
  (empty list if the maze is smaller than 9x7).
- `gen.get_dead_ends()` and `gen.count_loops()` give statistics about the maze.

### Accessing a solution

- `gen.find_shortest_path(start, end)` returns the list of cells of the
  shortest path.
- `gen.path_to_directions(path)` converts it to a `N`/`E`/`S`/`W` string.

### Building the package

From the root of the repository, in a clean virtual environment:

```bash
python3 -m virtualenv ~/venvs/build
source ~/venvs/build/bin/activate
pip install build
python3 -m build
ls dist
```

`python3 -m build` reads `pyproject.toml` and creates
`dist/mazegen-0.1.0-py3-none-any.whl` and `dist/mazegen-0.1.0.tar.gz`.
A built `mazegen-0.1.0-py3-none-any.whl` is also stored at the root of the
repository.

## Advanced features (bonuses)

- **Perfectly braided board**: in `PERFECT=False` mode the maze has no real
  dead-end at all. Confirmed by `maze_analyzer.py maze.txt --max-dead-ends 0`.
  Only the dead-ends enclosed by the "42" pattern remain, which the analyzer
  tolerates because they cannot be opened.
- **Animated generation**: press `a` to watch the maze being carved step by
  step (`MazeGenerator.generate_steps()` yields each step).
- **Extra display features**: the path is drawn with a colour gradient
  (green to red), and a cat can walk along the solution path to the fish.

## Team and project management

### Roles

The project was done entirely together by **ekarakas** and **arptadev**. Every
part (generation, output format, path finding, display, packaging) was written
in pair programming, explaining the code to each other so that both of us
understand the whole project.

### Planning and how it evolved

The initial plan was:

1. Configuration parser
2. Maze generation (DFS) and the grid structure
3. Hexadecimal output file
4. Shortest path (BFS)
5. Terminal display and user interactions
6. Reusable package and documentation

The plan mostly held, but some parts grew along the way: the display went
through several versions (ASCII `+--+`, block characters, then Unicode
box-drawing) until it looked clean and symmetric; the "42" pattern, the 3x3
open area rule and the error handling required more work than expected; and
the non-perfect mode was redesigned into a fully braided Pac-Man board.

### What worked well

- Pair programming: both of us can explain every part of the code.
- Testing every change with `maze_analyzer.py` on several sizes and seeds.
- Keeping one single generator class, used both by the program and the package.
- `flake8` and `mypy --strict` pass with no errors.

### What could be improved

- Support more generation algorithms (Prim's, Kruskal's) selectable from the
  configuration file.
- Add an automated test suite with `pytest` covering edge cases.
- Add a graphical display with MiniLibX in addition to the terminal one.

### Tools

- **git** and GitHub for version control
- **VS Code** as editor
- **flake8** and **mypy** for code style and static type checking
- **curses** (Python standard library) for the interactive terminal display
- **setuptools** and **build** for packaging
- `maze_analyzer.py` (provided with the subject) for validating the output

## Resources

- Jamis Buck, *Mazes for Programmers* (Pragmatic Bookshelf, 2015)
- Jamis Buck, "Maze Generation" blog series:
  <https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap>
- Wikipedia, "Maze generation algorithm":
  <https://en.wikipedia.org/wiki/Maze_generation_algorithm>
- Wikipedia, "Breadth-first search":
  <https://en.wikipedia.org/wiki/Breadth-first_search>
- Python documentation, `curses`:
  <https://docs.python.org/3/library/curses.html>
- Python documentation, `random` and `collections.deque`:
  <https://docs.python.org/3/library/random.html>
- Python Packaging User Guide:
  <https://packaging.python.org/en/latest/tutorials/packaging-projects/>
- Choose a License, MIT:
  <https://choosealicense.com/licenses/mit/>

### How AI was used

We used AI (Claude) as a teacher and reviewer during the whole project:

- **Learning**: explanations of DFS backtracking, BFS, braiding, the
  loop-counting formula (`passages - cells + 1`), `curses`, Python
  packaging, virtual environments and software licenses.
- **Code review**: checking the code against the subject, finding bugs and
  edge cases (small mazes, impossible parameters, huge sizes, file errors)
- **Code written with AI help**: the braiding methods (`is_dead_end`,
  `get_dead_ends`, `get_closed_neighbors`, `remove_dead_ends`) and
  `count_loops` were written by us step by step with AI guidance.
- **Documentation**: AI drafted this README, `mazegen/README.md` and the
  docstrings; we reviewed and corrected them.

## License

This project is released under the MIT License. See [LICENSE.md](LICENSE.md).
