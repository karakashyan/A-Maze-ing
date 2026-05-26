"""Maze generation logic for the A-Maze-ing project."""

import random


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

    def print_debug(self) -> None:
        """Print the maze grid for debugging."""
        for row in self.grid:
            print(row)
