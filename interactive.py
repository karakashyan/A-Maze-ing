"""Interactive terminal display for the A-Maze-ing project."""

import curses

from maze_generator import MazeGenerator
from renderer import render_maze_lines


def run_interactive(
    generator: MazeGenerator,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    path: list[tuple[int, int]],
) -> None:
    """Run interactive maze display."""

    def _main(stdscr: curses.window) -> None:
        current_generator = generator
        current_path = path
        current_seed = generator.seed
        show_path = True
        color_i = 1

        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(1, curses.COLOR_WHITE, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_CYAN, -1)
        curses.init_pair(4, curses.COLOR_YELLOW, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

        while True:
            stdscr.clear()

            if show_path:
                visible_path = current_path
            else:
                visible_path = []

            lines = render_maze_lines(
                current_generator,
                entry,
                exit_cell,
                visible_path,
            )
            try:
                for row_ind, line in enumerate(lines):
                    stdscr.addstr(row_ind, 0, line, curses.color_pair(color_i))

                for row, col in current_generator.get_42_cells():
                    if (row, col) == entry or (row, col) == exit_cell:
                        continue

                    screen_row = row * 2 + 1
                    screen_col = col * 4 + 1

                    stdscr.addstr(
                        screen_row,
                        screen_col,
                        "   ",
                        curses.color_pair(6),
                    )
                stdscr.addstr(
                    len(lines) + 1,
                    0,
                    "q - quit | p - show/hide path "
                    "| r - regenerate | c - colour",
                )
            except curses.error:
                pass

            stdscr.refresh()

            key = stdscr.getch()

            if key == ord("q"):
                break

            if key == ord("p"):
                show_path = not show_path

            if key == ord("r"):
                current_seed += 1
                current_generator = MazeGenerator(
                    current_generator.width,
                    current_generator.height,
                    current_seed,
                )
                current_generator.generate()
                current_generator.add_42_pattern(entry, exit_cell)
                current_path = current_generator.find_shortest_path(
                    entry,
                    exit_cell,
                )

            if key == ord("c"):
                color_i += 1
                if color_i > 5:
                    color_i = 1

    curses.wrapper(_main)
