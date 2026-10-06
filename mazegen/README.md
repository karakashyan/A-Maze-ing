*This project has been created as part of the 42 curriculum by ekarakas, arptadev.*

# mazegen

Reusable maze generator, created as part of the 42 A-Maze-ing project
by ekarakas and arptadev. Released under the MIT License.

The whole logic is a single class, `MazeGenerator`. It has no display and
no configuration file: you create it, generate a maze, and read the result.

## Installation

```bash
pip install mazegen-0.1.0-py3-none-any.whl
```

## Basic example

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
gen.generate()

entry = (0, 0)        # (row, col)
exit_cell = (14, 19)  # (row, col)
gen.add_42_pattern(entry, exit_cell)

path = gen.find_shortest_path(entry, exit_cell)
print(gen.path_to_directions(path))
```

## Custom parameters

| Parameter | Type   | Description                                         |
|-----------|--------|-----------------------------------------------------|
| `width`   | `int`  | Number of columns                                   |
| `height`  | `int`  | Number of rows                                      |
| `seed`    | `int`  | Random seed: the same seed gives the same maze      |
| `perfect` | `bool` | `True`: perfect maze (a single path, no loops)      |
|           |        | `False`: Pac-Man board (loops, no real dead-ends)   |

All coordinates used by the module are `(row, col)`.
If you work with `(x, y)` coordinates, then `x = col` and `y = row`.

## Accessing the generated structure

- `gen.grid[row][col]`: a dictionary of the four walls of a cell, for example
  `{"N": True, "E": False, "S": True, "W": True}`. `True` means the wall is
  closed. Neighbouring cells always agree on their shared wall.
- `gen.maze_to_hex_lines()`: the maze as a list of strings, one hexadecimal
  digit per cell (bit 0 = North, 1 = East, 2 = South, 3 = West,
  `1` = closed).
- `gen.save_hex(filename, entry, exit_cell, directions)`: write the maze, the
  entry, the exit and the path to a file.
- `gen.get_42_cells()`: the fully closed cells drawing "42"
  (empty list if the maze is smaller than 9x7, see `gen.can_draw_42()`).
- `gen.get_dead_ends()`: the dead-end cells.
- `gen.count_loops()`: the number of independent loops.

## Accessing a solution

- `gen.find_shortest_path(start, end)`: the shortest path (BFS) as a list of
  `(row, col)` cells, or an empty list if `end` cannot be reached.
- `gen.path_to_directions(path)`: the same path as a string of
  `N`, `E`, `S`, `W` letters.

## Animation

`gen.generate_steps()` is a generator version of `generate()`: it yields
`(current, next_cell)` each time a wall is removed, so a display can draw the
maze while it is being built.
