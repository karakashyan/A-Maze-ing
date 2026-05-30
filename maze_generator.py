"""Maze generation logic for the A-Maze-ing project."""

import random
from collections import deque


class MazeGenerator:
    """Generate and store a maze structure."""
    def __init__(self, width: int, height: int, seed: int) -> None:
        """Initialize the maze generator."""
        self.width = width
        self.height = height
        self.seed = seed
        self.grid = self._create_grid()
        self._42_cells = set(self.get_42_cells())

    def _create_grid(self) -> list[list[dict[str, bool]]]:
        """Create a grid where every cell starts with all walls closed."""
        grid = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                cell = {
                    "N": True,
                    "E": True,
                    "S": True,
                    "W": True,
                }
                row.append(cell)
            grid.append(row)
        return grid

    def remove_wall_between(self, c1: tuple[int, int],
                            c2: tuple[int, int]) -> None:
        """Remove the wall between two neighbouring cells."""
        row1, col1 = c1
        row2, col2 = c2

        cell1 = self.grid[row1][col1]
        cell2 = self.grid[row2][col2]

        if col2 == col1 + 1:
            cell1["E"] = False
            cell2["W"] = False
        elif col2 == col1 - 1:
            cell1["W"] = False
            cell2["E"] = False
        elif row2 == row1 + 1:
            cell1["S"] = False
            cell2["N"] = False
        elif row2 == row1 - 1:
            cell1["N"] = False
            cell2["S"] = False

    def get_neighbors(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        """Return all valid neighbours inside the maze bounds."""
        row, col = cell
        neighbors = []

        if row > 0:
            neighbor = (row - 1, col)
            if neighbor not in self._42_cells:
                neighbors.append(neighbor)
        if row < self.height - 1:
            neighbor = (row + 1, col)
            if neighbor not in self._42_cells:
                neighbors.append(neighbor)
        if col > 0:
            neighbor = (row, col - 1)
            if neighbor not in self._42_cells:
                neighbors.append(neighbor)
        if col < self.width - 1:
            neighbor = (row, col + 1)
            if neighbor not in self._42_cells:
                neighbors.append(neighbor)
        return neighbors

    def generate(self) -> None:
        """Generate a perfect maze using an iterative backtracking."""
        random.seed(self.seed)

        start = (0, 0)
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        visited.add(start)
        stack.append(start)
        while stack:
            current = stack[-1]
            unvisited_neighbors = []
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    unvisited_neighbors.append(neighbor)

            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                self.remove_wall_between(current, next_cell)
                visited.add(next_cell)
                stack.append(next_cell)
            else:
                stack.pop()

    def generate_steps(self):
        """Generate maze step-by-step for animation (curses-friendly)."""
        random.seed(self.seed)

        start = (0, 0)
        visited: set[tuple[int, int]] = {start}
        stack: list[tuple[int, int]] = [start]

        while stack:
            current = stack[-1]

            unvisited_neighbors = [
                n for n in self.get_neighbors(current)
                if n not in visited
            ]

            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)

                self.remove_wall_between(current, next_cell)

                yield current, next_cell

                visited.add(next_cell)
                stack.append(next_cell)
            else:
                stack.pop()

    def get_42_cells(self) -> list[tuple[int, int]]:
        """Return cells used to draw the 42 pattern."""
        start_row = (self.height - 5) // 2
        start_col = (self.width - 7) // 2
        cells = [
            (0, 0), (0, 4), (0, 5), (0, 6),
            (1, 0), (1, 6),
            (2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2, 6),
            (3, 2), (3, 4),
            (4, 2), (4, 4), (4, 5), (4, 6),
        ]
        real_cells = []
        for row, col in cells:
            real_cells.append((start_row + row, start_col + col))
        return real_cells

    def validate_e_x(self, e: tuple[int, int], x: tuple[int, int]) -> bool:
        """Return True if entry and exit do not overlap with the 42 pattern."""
        return e not in self._42_cells and x not in self._42_cells

    def add_42_pattern(
        self,
        entry: tuple[int, int],
        exit_cell: tuple[int, int],
    ) -> None:
        """Add a visible 42 pattern using fully closed cells."""
        if self.width < 7 or self.height < 5:
            print("Warning: maze is too small for the 42 pattern!")
            return
        cells = self.get_42_cells()
        for c in cells:
            if c == entry or c == exit_cell:
                continue
            self.close_cell(c)

    def close_cell(self, cell: tuple[int, int]) -> None:
        """Close all walls around one cell and update neighbouring walls."""
        row, col = cell

        self.grid[row][col]["N"] = True
        self.grid[row][col]["E"] = True
        self.grid[row][col]["S"] = True
        self.grid[row][col]["W"] = True

        if row > 0:
            self.grid[row - 1][col]["S"] = True
        if col < self.width - 1:
            self.grid[row][col + 1]["W"] = True
        if row < self.height - 1:
            self.grid[row + 1][col]["N"] = True
        if col > 0:
            self.grid[row][col - 1]["E"] = True

    def cell_to_hex(self, cell: dict[str, bool]) -> str:
        """Convert one maze cell to a hexadecimal wall value."""
        value = 0

        if cell["N"]:
            value += 1
        if cell["E"]:
            value += 2
        if cell["S"]:
            value += 4
        if cell["W"]:
            value += 8

        return format(value, "X")

    def row_to_hex(self, row: list[dict[str, bool]]) -> str:
        """Convert one maze row to a hexadecimal string."""
        return "".join(self.cell_to_hex(cell) for cell in row)

    def maze_to_hex_lines(self) -> list[str]:
        """Convert the whole maze grid to hexadecimal lines."""
        result = []
        for row in self.grid:
            result.append(self.row_to_hex(row))
        return result

    def save_hex(
        self,
        filename: str,
        entry: tuple[int, int],
        exit_cell: tuple[int, int],
        path_directions: str,
    ) -> None:
        """Save the maze grid to a file in hexadecimal format."""
        with open(filename, "w", encoding="utf-8") as file:
            for line in self.maze_to_hex_lines():
                file.write(line + "\n")
            file.write("\n")
            for row, col in (entry, exit_cell):
                file.write(f"{col},{row}\n")
            file.write(path_directions + "\n")

    def get_open_neighbors(
        self,
        cell: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Return reachable neighbours through open walls."""
        row, col = cell
        cell_walls = self.grid[row][col]
        neighbors = []

        if not cell_walls["N"] and row > 0:
            neighbor = (row - 1, col)
            if neighbor not in self._42_cells:
                neighbors.append(neighbor)

        if not cell_walls["E"] and col < self.width - 1:
            neighbor = (row, col + 1)
            if neighbor not in self._42_cells:
                neighbors.append(neighbor)

        if not cell_walls["S"] and row < self.height - 1:
            neighbor = (row + 1, col)
            if neighbor not in self._42_cells:
                neighbors.append(neighbor)

        if not cell_walls["W"] and col > 0:
            neighbor = (row, col - 1)
            if neighbor not in self._42_cells:
                neighbors.append(neighbor)

        return neighbors

    def find_shortest_path(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Find the shortest path between two cells."""
        queue = deque([start])
        visited: set[tuple[int, int]] = {start}
        parent: dict[tuple[int, int], tuple[int, int]] = {}

        while queue:
            current = queue.popleft()

            if current == end:
                break

            for neighbor in self.get_open_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        if end not in parent and start != end:
            return []

        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])

        path.reverse()
        return path

    def path_to_directions(self, path: list[tuple[int, int]]) -> str:
        """Convert a cell path to N/E/S/W directions."""
        result = ""

        for i in range(len(path) - 1):
            row1, col1 = path[i]
            row2, col2 = path[i + 1]

            if col2 == col1 + 1:
                result += "E"
            elif col2 == col1 - 1:
                result += "W"
            elif row2 == row1 + 1:
                result += "S"
            elif row2 == row1 - 1:
                result += "N"

        return result

    def print_debug(self) -> None:
        """Print the maze grid for debugging."""
        for row in self.grid:
            print(row)
