from maze_generator import MazeGenerator


def render_maze(
    generator: MazeGenerator,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    path: list[tuple[int, int]],
) -> None:
    """Print the maze in ASCII format."""
    for line in render_maze_lines(generator, entry, exit_cell, path):
        print(line)


def render_maze_lines(
    generator: MazeGenerator,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    path: list[tuple[int, int]],
) -> list[str]:
    """Build ASCII maze lines."""
    path_set = set(path)
    maze_lines = []

    top = "+"
    for _ in range(generator.width):
        top += "---+"
    maze_lines.append(top)

    for i in range(generator.height):
        result = ""
        for j in range(generator.width):
            cell_pos = (i, j)

            if generator.grid[i][j]["W"]:
                result += "|"
            else:
                result += " "

            if cell_pos == entry:
                result += " E "
            elif cell_pos == exit_cell:
                result += " X "
            elif cell_pos in path_set:
                result += " * "
            else:
                result += "   "

        result += "|"
        maze_lines.append(result)

        result = ""
        for j in range(generator.width):
            result += "+"
            if generator.grid[i][j]["S"]:
                result += "---"
            else:
                result += "   "

        result += "+"
        maze_lines.append(result)

    return maze_lines
