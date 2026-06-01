"""Interactive terminal display for the A-Maze-ing project."""

import curses
from maze_generator import MazeGenerator
from renderer import render_maze_lines

_WALL = 1
_ENTRY = 7
_EXIT = 8
_PATH_A = 9
_PATH_B = 10
_PATH_C = 11
_42 = 12
_BAR = 13

_WALL_COLORS = [
    curses.COLOR_WHITE,
    curses.COLOR_CYAN,
    curses.COLOR_GREEN,
    curses.COLOR_YELLOW,
    curses.COLOR_MAGENTA,
    curses.COLOR_BLUE,
]

_PATH_DOTS = ["·", "•", "◆"]
ENTRY_LABEL = " E "
EXIT_LABEL = " X "
ANIMAL_LABEL = "🐱 "
FOOD_LABEL = "🐟 "


def _path_pair(idx: int, length: int) -> int:
    """Return the color pair index for a path cell based on its progress."""

    if length == 0:
        return _PATH_A
    progress = idx / length
    if progress < 0.4:
        return _PATH_A
    if progress < 0.75:
        return _PATH_B
    return _PATH_C


def run_interactive(
    generator: MazeGenerator,
    entry: tuple[int, int],
    exit_cell: tuple[int, int],
    path: list[tuple[int, int]],
) -> None:
    """Launch the curses display loop for the maze."""

    def _main(stdscr: curses.window) -> None:
        """Draw and handle the curses event loop."""
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)
        stdscr.timeout(60)

        curses.init_pair(_ENTRY,  curses.COLOR_GREEN,  -1)
        curses.init_pair(_EXIT,   curses.COLOR_RED,    -1)
        curses.init_pair(_PATH_A, curses.COLOR_GREEN,  -1)
        curses.init_pair(_PATH_B, curses.COLOR_YELLOW, -1)
        curses.init_pair(_PATH_C, curses.COLOR_RED,    -1)
        curses.init_pair(_42,     curses.COLOR_WHITE,  curses.COLOR_BLUE)
        curses.init_pair(_BAR,    curses.COLOR_BLACK,  curses.COLOR_WHITE)

        cur_gen = generator
        cur_path = path
        cur_seed = generator.seed
        cur_perfect = generator.perfect
        show_path = True
        wall_i = 0
        animate = False
        animal_pos = entry
        food_visible = True
        move_animation = False
        move_index = 0
        move_delay = 0

        def regenerate() -> None:
            """Regenerate the maze, optionally with animation."""
            nonlocal cur_gen, cur_path
            nonlocal animal_pos, food_visible
            nonlocal move_animation, move_index, move_delay

            cur_gen = MazeGenerator(
                cur_gen.width,
                cur_gen.height,
                cur_seed,
                cur_perfect,
            )

            if animate:
                for _ in cur_gen.generate_steps():
                    stdscr.erase()

                    lines = render_maze_lines(cur_gen, entry, exit_cell, [])

                    for row_i, line in enumerate(lines):
                        stdscr.addstr(row_i, 0, line)

                    stdscr.refresh()
                    curses.napms(20)
            else:
                cur_gen.generate()

            cur_gen.add_42_pattern(entry, exit_cell)
            cur_path = cur_gen.find_shortest_path(entry, exit_cell)

            animal_pos = entry
            food_visible = True
            move_animation = False
            move_index = 0
            move_delay = 0

        def _init_wall_pair() -> None:
            """Initialize the current wall colour pair."""
            curses.init_pair(_WALL, _WALL_COLORS[wall_i], -1)

        _init_wall_pair()

        while True:
            stdscr.erase()
            _init_wall_pair()

            vis_path = cur_path if show_path else []
            path_index = {cell: idx for idx, cell in enumerate(vis_path)}
            path_len = max(len(vis_path) - 1, 1)
            lines = render_maze_lines(cur_gen, entry, exit_cell, vis_path)

            try:
                wall_attr = curses.color_pair(_WALL)
                outer_attr = wall_attr | curses.A_BOLD

                for row_i, line in enumerate(lines):
                    stdscr.addstr(row_i, 0, line, wall_attr)

                for r in range(cur_gen.height):
                    screen_row = r * 2 + 1
                    for c in range(cur_gen.width):
                        screen_col = c * 4 + 1
                        cell = (r, c)
                        if cell == animal_pos:
                            stdscr.addstr(
                                screen_row, screen_col, ANIMAL_LABEL,
                                curses.A_BOLD,
                            )
                        elif cell == exit_cell and food_visible:
                            stdscr.addstr(
                                screen_row, screen_col, FOOD_LABEL,
                                curses.A_BOLD,
                            )
                        elif cell == entry:
                            stdscr.addstr(
                                screen_row, screen_col, ENTRY_LABEL,
                                curses.color_pair(_ENTRY)
                                | curses.A_REVERSE | curses.A_BOLD,
                            )
                        elif cell == exit_cell:
                            stdscr.addstr(
                                screen_row, screen_col, EXIT_LABEL,
                                curses.color_pair(_EXIT)
                                | curses.A_REVERSE | curses.A_BOLD,
                            )
                        elif cell in path_index:
                            idx = path_index[cell]
                            dot = _PATH_DOTS[min(int(idx / path_len * 3), 2)]
                            pair = _path_pair(idx, path_len)
                            stdscr.addstr(screen_row, screen_col,
                                          f" {dot} ", curses.color_pair(pair))

                for row, col in cur_gen.get_42_cells():
                    if (row, col) in (entry, exit_cell):
                        continue
                    stdscr.addstr(row * 2 + 1, col * 4 + 1, " ✦ ",
                                  curses.color_pair(_42))

                stdscr.addstr(0, 0, lines[0], outer_attr)
                stdscr.addstr(len(lines) - 1, 0, lines[-1], outer_attr)
                for row_i in range(1, len(lines) - 1):
                    line = lines[row_i]
                    stdscr.addstr(row_i, 0, line[0], outer_attr)
                    stdscr.addstr(row_i, len(line) - 1, line[-1], outer_attr)

                menu_y = len(lines) + 1
                path_status = "ON" if show_path else "OFF"

                stdscr.addstr(
                    menu_y, 0, "=== A-Maze-ing ===", curses.color_pair(_BAR))
                stdscr.addstr(menu_y + 1, 0, f"Seed: {cur_seed}")

                stdscr.addstr(menu_y + 3, 0, "r - Re-generate a new maze")
                stdscr.addstr(menu_y + 4, 0, "p - Show/Hide path "
                              f"from entry to exit ({path_status})")
                stdscr.addstr(menu_y + 5, 0, "c - Rotate maze colors")
                stdscr.addstr(menu_y + 6, 0, "a - Animated regenerate "
                              f"({'ON' if animate else 'OFF'})")
                stdscr.addstr(menu_y + 7, 0, "m - Move animal to food")
                stdscr.addstr(menu_y + 8, 0, "q - Quit")
            except curses.error:
                pass

            stdscr.refresh()

            if move_animation and cur_path:
                move_delay += 1

                if move_delay >= 2:
                    move_delay = 0

                    if move_index < len(cur_path):
                        animal_pos = cur_path[move_index]
                        move_index += 1

                        if animal_pos == exit_cell:
                            food_visible = False
                            move_animation = False
                    else:
                        food_visible = False
                        move_animation = False

            key = stdscr.getch()

            if key == ord("q"):
                break
            elif key == ord("p"):
                show_path = not show_path
            elif key == ord("a"):
                animate = not animate
                cur_seed += 1
                regenerate()
            elif key == ord("r"):
                cur_seed += 1
                regenerate()
            elif key == ord("m"):
                if cur_path:
                    animal_pos = entry
                    food_visible = True
                    move_animation = True
                    move_index = 0
                    move_delay = 0
            elif key == ord("c"):
                wall_i = (wall_i + 1) % len(_WALL_COLORS)

    curses.wrapper(_main)
