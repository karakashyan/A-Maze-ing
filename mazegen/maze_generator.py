"""Maze generation logic for the A-Maze-ing project.

This module provides the reusable ``MazeGenerator`` class. All coordinates
used by the module are ``(row, col)`` tuples.
"""

import random
from collections import deque
from collections.abc import Iterator


class MazeGenerator:
    """Generate and store a maze structure.

    Each cell of ``grid`` is a dictionary of four walls (``"N"``, ``"E"``,
    ``"S"``, ``"W"``). ``True`` means the wall is closed, ``False`` means it
    is open. Neighbouring cells always agree on their shared wall.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        seed: Random seed, the same seed always gives the same maze.
        perfect: ``True`` for a perfect maze (a single path, no loops),
            ``False`` for a Pac-Man board (loops and no real dead-ends).
        grid: The maze, accessed as ``grid[row][col]``.
    """

    def __init__(self, width: int, height: int,
                 seed: int, perfect: bool) -> None:
        """Initialize the generator with every wall closed.

        Args:
            width: Number of columns.
            height: Number of rows.
            seed: Random seed used by ``generate``.
            perfect: ``True`` for a perfect maze, ``False`` for a
                Pac-Man board.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.grid = self._create_grid()
        self._42_cells = set(self.get_42_cells())
        self.perfect = perfect

    def _create_grid(self) -> list[list[dict[str, bool]]]:
        """Create a grid where every cell starts with all walls closed.

        Returns:
            A ``height`` x ``width`` list of wall dictionaries.
        """
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
        """Remove the wall between two neighbouring cells.

        Both cells are updated, so the shared wall stays coherent.

        Args:
            c1: First cell as ``(row, col)``.
            c2: Second cell as ``(row, col)``, next to ``c1``.
        """
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
        """Return the neighbours of a cell, ignoring walls.

        Cells outside the maze and cells of the "42" pattern are skipped.

        Args:
            cell: The cell as ``(row, col)``.

        Returns:
            The list of neighbouring cells.
        """
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
        """Generate the maze; remove dead ends if it is not perfect.

        Uses an iterative randomized depth-first search (recursive
        backtracker). If ``perfect`` is ``False``, ``remove_dead_ends`` is
        then applied to turn the maze into a braided Pac-Man board.
        """
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
        """Generate the maze step by step, for animation.

        Works like ``generate`` but pauses each time a wall is removed.

        Yields:
            ``(current, next_cell)``: the two cells whose shared wall
            has just been removed.
        """
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

    def can_draw_42(self) -> bool:
        """Check whether the maze is large enough for the "42" pattern.

        Returns:
            ``True`` if the maze is at least 9 x 7 cells.
        """
        return self.width >= 9 and self.height >= 7

    def get_42_cells(self) -> list[tuple[int, int]]:
        """Return the cells used to draw the "42" pattern.

        The pattern is 7 x 5 cells and is centred in the maze.

        Returns:
            The list of "42" cells, or an empty list if the maze is too
            small (see ``can_draw_42``).
        """
        real_cells: list[tuple[int, int]] = []
        if not self.can_draw_42():
            return real_cells
        start_row = (self.height - 5) // 2
        start_col = (self.width - 7) // 2
        cells = [
            (0, 0), (0, 4), (0, 5), (0, 6),
            (1, 0), (1, 6),
            (2, 0), (2, 1), (2, 2), (2, 4), (2, 5), (2, 6),
            (3, 2), (3, 4),
            (4, 2), (4, 4), (4, 5), (4, 6),
        ]
        for row, col in cells:
            real_cells.append((start_row + row, start_col + col))
        return real_cells

    def validate_e_x(self, entry: tuple[int, int],
                     exit_cell: tuple[int, int]) -> bool:
        """Check that the entry and the exit are not "42" cells.

        Args:
            entry: Entry cell as ``(row, col)``.
            exit_cell: Exit cell as ``(row, col)``.

        Returns:
            ``True`` if neither cell overlaps the "42" pattern.
        """
        return entry not in self._42_cells and exit_cell not in self._42_cells

    def add_42_pattern(
        self,
        entry: tuple[int, int],
        exit_cell: tuple[int, int],
    ) -> None:
        """Draw the visible "42" pattern with fully closed cells.

        Does nothing if the maze is too small (see ``can_draw_42``).

        Args:
            entry: Entry cell as ``(row, col)``, never closed.
            exit_cell: Exit cell as ``(row, col)``, never closed.
        """
        if not self.can_draw_42():
            return
        cells = self.get_42_cells()
        for c in cells:
            if c == entry or c == exit_cell:
                continue
            self.close_cell(c)

    def close_cell(self, cell: tuple[int, int]) -> None:
        """Close all walls of a cell and update its neighbours.

        Args:
            cell: The cell to close, as ``(row, col)``.
        """
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
        """Check whether opening a wall would create a 3 x 3 open area.

        The wall is opened temporarily, every 3 x 3 square around it is
        checked, then the wall is restored. The maze is not changed.

        Args:
            c1: First cell as ``(row, col)``.
            c2: Second cell as ``(row, col)``, next to ``c1``.

        Returns:
            ``True`` if opening the wall would create a 3 x 3 open area.
        """
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
        """Convert one cell to its hexadecimal wall value.

        Bit 0 = North, 1 = East, 2 = South, 3 = West; a set bit means
        the wall is closed.

        Args:
            cell: The wall dictionary of the cell.

        Returns:
            One uppercase hexadecimal digit, from ``"0"`` to ``"F"``.
        """
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
        """Convert one maze row to a hexadecimal string.

        Args:
            row: The list of wall dictionaries of the row.

        Returns:
            One hexadecimal digit per cell.
        """
        return "".join(self.cell_to_hex(cell) for cell in row)

    def maze_to_hex_lines(self) -> list[str]:
        """Convert the whole maze to hexadecimal lines.

        Returns:
            One string per row, one hexadecimal digit per cell.
        """
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
        """Save the maze to a file in the hexadecimal format.

        The file contains the grid, an empty line, the entry and exit as
        ``x,y`` and the path as ``N``/``E``/``S``/``W`` letters.

        Args:
            filename: Path of the output file.
            entry: Entry cell as ``(row, col)``.
            exit_cell: Exit cell as ``(row, col)``.
            path_directions: The path, for example ``"SSEEN"``.

        Raises:
            OSError: If the file cannot be written.
        """
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
        """Return the neighbours reachable through an open wall.

        Args:
            cell: The cell as ``(row, col)``.

        Returns:
            The list of neighbouring cells with no wall in between.
        """
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
        """Find the shortest path between two cells using BFS.

        Args:
            start: Start cell as ``(row, col)``.
            end: End cell as ``(row, col)``.

        Returns:
            The cells of the path from ``start`` to ``end`` (both
            included), or an empty list if ``end`` cannot be reached.
        """
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
        """Convert a path of cells to direction letters.

        Args:
            path: The cells of the path, as returned by
                ``find_shortest_path``.

        Returns:
            A string of ``N``, ``E``, ``S``, ``W`` letters.
        """
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
        """Check whether a cell is a dead end.

        Args:
            cell: The cell as ``(row, col)``.

        Returns:
            ``True`` if the cell has exactly one open wall.
        """
        row, col = cell
        return list(self.grid[row][col].values()).count(False) == 1

    def get_dead_ends(self) -> list[tuple[int, int]]:
        """Return all dead-end cells of the maze.

        Returns:
            The list of dead-end cells as ``(row, col)``.
        """
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
        """Return the neighbours separated from the cell by a wall.

        The outer border and the "42" cells are never included.

        Args:
            cell: The cell as ``(row, col)``.

        Returns:
            The list of neighbouring cells behind a closed wall.
        """
        opened = self.get_open_neighbors(cell)
        closed: list[tuple[int, int]] = []
        for c in self.get_neighbors(cell):
            if c not in opened:
                closed.append(c)
        return closed

    def remove_dead_ends(self) -> None:
        """Open extra walls so that the maze has no dead ends (braiding).

        For each dead end, one closed wall is opened towards a random
        neighbour. A wall is never opened if it would create a 3 x 3 open
        area, so a few dead ends may remain in very tight spots.
        """
        ends = self.get_dead_ends()
        for cell in ends:
            if not self.is_dead_end(cell):
                continue
            closed = self.get_closed_neighbors(cell)
            safe: list[tuple[int, int]] = []
            for n in closed:
                if not self.would_create_3x3_open_area(cell, n):
                    safe.append(n)
            if not safe:
                continue
            neighbor = random.choice(safe)
            self.remove_wall_between(cell, neighbor)

    def count_loops(self) -> int:
        """Count the independent loops of the maze.

        Uses the formula ``passages - cells + 1``. Each passage is counted
        once by looking only at the east and south walls.

        Returns:
            The number of independent loops (0 for a perfect maze).
        """
        cells = self.width * self.height - len(self._42_cells)
        passages = 0
        for row in range(self.height):
            for col in range(self.width):
                if not self.grid[row][col]["E"]:
                    passages += 1
                if not self.grid[row][col]["S"]:
                    passages += 1
        return passages - cells + 1
