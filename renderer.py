"""Unicode renderer for the A-Maze-ing project.

Turns a ``MazeGenerator`` grid into lines of box-drawing characters.
Each cell is 4 characters wide (1 wall + 3 inside) and 2 lines high.
"""

from mazegen import MazeGenerator

_INNER_JOINTS = {
    (False, False, False, False): " ",
    (True,  False, False, False): "╵",
    (False, True,  False, False): "╷",
    (True,  True,  False, False): "│",
    (False, False, True,  False): "╴",
    (False, False, False, True): "╶",
    (False, False, True,  True): "─",
    (True,  False, True,  False): "┘",
    (True,  False, False, True): "└",
    (False, True,  True,  False): "┐",
    (False, True,  False, True): "┌",
    (True,  True,  True,  False): "┤",
    (True,  True,  False, True): "├",
    (True,  False, True,  True): "┴",
    (False, True,  True,  True): "┬",
    (True,  True,  True,  True): "┼",
}

_PATH_DOTS = ["·", "•", "◆"]

Grid = list[list[dict[str, bool]]]


def _cell_wall(
    grid: Grid,
    row: int,
    col: int,
    direction: str,
    height: int,
    width: int,
) -> bool:
    """Return the wall flag of a cell in one direction.

    Args:
        grid: The maze grid.
        row: Row of the cell.
        col: Column of the cell.
        direction: One of ``"N"``, ``"E"``, ``"S"``, ``"W"``.
        height: Number of rows of the maze.
        width: Number of columns of the maze.

    Returns:
        ``True`` if the wall is closed, ``False`` if it is open or if the
        cell is outside the maze.
    """
    if row < 0 or row >= height or col < 0 or col >= width:
        return False
    return bool(grid[row][col][direction])


def _inner_joint(
    grid: Grid,
    i: int,
    j: int,
    height: int,
    width: int,
) -> str:
    """Return the box-drawing character for an interior corner.

    The corner is the point between cells ``(i - 1, j - 1)``,
    ``(i - 1, j)``, ``(i, j - 1)`` and ``(i, j)``.

    Args:
        grid: The maze grid.
        i: Row index of the corner.
        j: Column index of the corner.
        height: Number of rows of the maze.
        width: Number of columns of the maze.

    Returns:
        One box-drawing character, for example ``"┼"`` or ``"└"``.
    """
    north = _cell_wall(grid, i - 1, j - 1, "E", height, width)
    south = _cell_wall(grid, i,     j - 1, "E", height, width)
    west = _cell_wall(grid, i - 1, j - 1, "S", height, width)
    east = _cell_wall(grid, i - 1, j,     "S", height, width)
    return _INNER_JOINTS.get((north, south, west, east), "?")


def _top_joint(grid: Grid, j: int) -> str:
    """Return the top border character between two columns.

    Args:
        grid: The maze grid.
        j: Column on the right of the joint.

    Returns:
        ``"╤"`` if a vertical wall starts here, ``"═"`` otherwise.
    """
    if grid[0][j]["W"]:
        return "╤"
    return "═"


def _bottom_joint(grid: Grid, j: int, height: int) -> str:
    """Return the bottom border character between two columns.

    Args:
        grid: The maze grid.
        j: Column on the right of the joint.
        height: Number of rows of the maze.

    Returns:
        ``"╧"`` if a vertical wall ends here, ``"═"`` otherwise.
    """
    if grid[height - 1][j]["W"]:
        return "╧"
    return "═"


def render_maze_lines(
    generator: MazeGenerator,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    path: list[tuple[int, int]],
) -> list[str]:
    """Build the maze as a list of Unicode strings.

    Entry and exit cells are left empty: the interactive display draws
    them on top with colours.

    Args:
        generator: The generated maze.
        entry: Entry cell as ``(row, col)``.
        exit_cell: Exit cell as ``(row, col)``.
        path: Cells of the path to draw, or an empty list to hide it.

    Returns:
        The lines of the drawing, ``2 * height + 1`` lines in total.
    """
    path_index = {cell: idx for idx, cell in enumerate(path)}
    path_len = max(len(path) - 1, 1)
    maze_lines = []
    H, W = generator.height, generator.width
    grid = generator.grid

    top = "╔═══"
    for j in range(1, W):
        top += _top_joint(grid, j)
        top += "═══"
    top += "╗"
    maze_lines.append(top)

    for i in range(H):
        row = ""
        for j in range(W):
            if j == 0:
                row += "║"
            elif grid[i][j]["W"]:
                row += "│"
            else:
                row += " "

            cell_pos = (i, j)
            if cell_pos == entry:
                row += "   "
            elif cell_pos == exit_cell:
                row += "   "
            elif cell_pos in path_index:
                idx = path_index[cell_pos]
                dot = _PATH_DOTS[min(int(idx / path_len * 3), 2)]
                row += f" {dot} "
            else:
                row += "   "

        row += "║"
        maze_lines.append(row)

        if i == H - 1:
            bot = "╚═══"
            for j in range(1, W):
                bot += _bottom_joint(grid, j, H)
                bot += "═══"
            bot += "╝"
            maze_lines.append(bot)
        else:
            sep = ""
            for j in range(W):
                if j == 0:
                    sep += "╟" if grid[i][j]["S"] else "║"
                else:
                    sep += _inner_joint(grid, i + 1, j, H, W)
                sep += "───" if grid[i][j]["S"] else "   "
            sep += "╢" if grid[i][W - 1]["S"] else "║"
            maze_lines.append(sep)

    return maze_lines


def render_maze(
    generator: MazeGenerator,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    path: list[tuple[int, int]],
) -> None:
    """Print the maze to the terminal in Unicode box-drawing format.

    Args:
        generator: The generated maze.
        entry: Entry cell as ``(row, col)``.
        exit_cell: Exit cell as ``(row, col)``.
        path: Cells of the path to draw, or an empty list to hide it.
    """
    for line in render_maze_lines(generator, entry, exit_cell, path):
        print(line)
