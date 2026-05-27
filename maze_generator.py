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
            neighbors.append((row - 1, col))
        if row < self.height - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < self.width - 1:
            neighbors.append((row, col + 1))
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
                entry_str = f"{row},{col}\n"
                file.write(entry_str)
            file.write(path_directions)

    def get_open_neighbors(
        self,
        cell: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Return reachable neighbours through open walls."""
        row, col = cell
        cell_walls = self.grid[row][col]
        neighbors = []

        if not cell_walls["N"] and row > 0:
            neighbors.append((row - 1, col))

        if not cell_walls["E"] and col < self.width - 1:
            neighbors.append((row, col + 1))

        if not cell_walls["S"] and row < self.height - 1:
            neighbors.append((row + 1, col))

        if not cell_walls["W"] and col > 0:
            neighbors.append((row, col - 1))

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
