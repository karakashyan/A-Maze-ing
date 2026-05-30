from maze_generator import MazeGenerator

_INNER_JOINTS = {
    (False, False, False, False): " ",
    (True,  False, False, False): "╵",
    (False, True,  False, False): "╷",
    (True,  True,  False, False): "│",
    (False, False, True,  False): "╴",
    (False, False, False, True ): "╶",
    (False, False, True,  True ): "─",
    (True,  False, True,  False): "┘",
    (True,  False, False, True ): "└",
    (False, True,  True,  False): "┐",
    (False, True,  False, True ): "┌",
    (True,  True,  True,  False): "┤",
    (True,  True,  False, True ): "├",
    (True,  False, True,  True ): "┴",
    (False, True,  True,  True ): "┬",
    (True,  True,  True,  True ): "┼",
}

_PATH_DOTS = ["·", "•", "◆"]


def _cell_wall(grid, row, col, direction, height, width):
    """Return the wall flag for cell (row, col) in the given direction."""
    if row < 0 or row >= height or col < 0 or col >= width:
        return False
    return bool(grid[row][col][direction])


def _inner_joint(grid, i, j, height, width):
    """Return the box-drawing character for the interior corner at (i, j)."""
    north = _cell_wall(grid, i - 1, j - 1, "E", height, width)
    south = _cell_wall(grid, i,     j - 1, "E", height, width)
    west  = _cell_wall(grid, i - 1, j - 1, "S", height, width)
    east  = _cell_wall(grid, i - 1, j,     "S", height, width)
    return _INNER_JOINTS.get((north, south, west, east), "?")


def _top_joint(grid, j):
    """Return the border character between columns j-1 and j on the top edge."""
    if grid[0][j]["W"]:
        return "╤"
    return "═"


def _bottom_joint(grid, j, height):
    """Return the border character between columns j-1 and j on the bottom edge."""
    if grid[height - 1][j]["W"]:
        return "╧"
    return "═"


def render_maze_lines(generator, entry, exit_cell, path):
    """Build and return the maze as a list of Unicode strings."""
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


def render_maze(generator, entry, exit_cell, path):
    """Print the maze to stdout in Unicode box-drawing format."""
    for line in render_maze_lines(generator, entry, exit_cell, path):
        print(line)
