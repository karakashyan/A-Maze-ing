"""Maze generation logic for the A-Maze-ing project."""

import random
from collections import deque
from collections.abc import Iterator


class MazeGenerator:
    """Generate and store a maze structure."""
    def __init__(self, width: int, height: int,
                 seed: int, perfect: bool) -> None:
        """Initialize the maze generator."""
        self.width = width
        self.height = height
        self.seed = seed
        self.grid = self._create_grid()
        self._42_cells = set(self.get_42_cells())
        self.perfect = perfect

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

        if not self.perfect:
            self.remove_dead_ends()

    def generate_steps(
            self) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
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

        if not self.perfect:
            self.remove_dead_ends()

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

    def would_create_3x3_open_area(
        self,
        c1: tuple[int, int],
        c2: tuple[int, int],
    ) -> bool:
        """Return True if opening this wall creates a 3x3 open area."""
        row1, col1 = c1
        row2, col2 = c2

        old_cell1 = self.grid[row1][col1].copy()
        old_cell2 = self.grid[row2][col2].copy()

        self.remove_wall_between(c1, c2)

        min_row = max(0, min(row1, row2) - 2)
        max_row = min(self.height - 3, max(row1, row2))
        min_col = max(0, min(col1, col2) - 2)
        max_col = min(self.width - 3, max(col1, col2))

        for start_row in range(min_row, max_row + 1):
            for start_col in range(min_col, max_col + 1):
                is_open = True

                for row in range(start_row, start_row + 3):
                    for col in range(start_col, start_col + 2):
                        if self.grid[row][col]["E"]:
                            is_open = False

                for row in range(start_row, start_row + 2):
                    for col in range(start_col, start_col + 3):
                        if self.grid[row][col]["S"]:
                            is_open = False

                if is_open:
                    self.grid[row1][col1] = old_cell1
                    self.grid[row2][col2] = old_cell2
                    return True

        self.grid[row1][col1] = old_cell1
        self.grid[row2][col2] = old_cell2

        return False

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

    def is_dead_end(self, cell: tuple[int, int]) -> bool:
        """Return True if the cell has exactly one open wall."""
        row, col = cell
        return list(self.grid[row][col].values()).count(False) == 1

    def get_dead_ends(self) -> list[tuple[int, int]]:
        """Return all dead-end cells of the maze."""
        dead_ends: list[tuple[int, int]] = []
        for row in range(self.height):
            for col in range(self.width):
                if self.is_dead_end((row, col)):
                    dead_ends.append((row, col))
        return dead_ends

    def get_closed_neighbors(
        self,
        cell: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Return valid neighbours separated from the cell by a wall."""
        opened = self.get_open_neighbors(cell)
        closed: list[tuple[int, int]] = []
        for c in self.get_neighbors(cell):
            if c not in opened:
                closed.append(c)
        return closed

    def remove_dead_ends(self) -> None:
        """Open extra walls so that the maze has no dead ends."""
        ends = self.get_dead_ends()
        for cell in ends:
            if not self.is_dead_end(cell):
                continue
            closed = self.get_closed_neighbors(cell)
            if not closed:
                continue
            neighbor = random.choice(closed)
            self.remove_wall_between(cell, neighbor)
