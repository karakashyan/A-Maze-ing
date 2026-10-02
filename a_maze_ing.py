"""Main entry point for the A-Maze-ing project."""

import curses
import sys
from config_parser import load_config
from mazegen import MazeGenerator
from interactive import run_interactive


def main() -> None:
    """Run the maze generator program."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config_file = sys.argv[1]

    try:
        config = load_config(config_file)
    except FileNotFoundError:
        print(f"Error: file not found: {config_file}")
        return
    except ValueError as error:
        print(f"Error: {error}")
        return
    except KeyError as error:
        print(f"Error: missing required key: {error}")
        return

    if config["width"] < 7 or config["height"] < 5:
        print("Error: maze is too small for the 42 pattern")
        return

    generator = MazeGenerator(
        width=config["width"],
        height=config["height"],
        seed=config["seed"],
        perfect=config["perfect"]
    )

    generator.generate()

    entry_col, entry_row = config["entry"]
    exit_col, exit_row = config["exit"]

    entry = (entry_row, entry_col)
    exit_cell = (exit_row, exit_col)

    if not generator.validate_e_x(entry, exit_cell):
        print("Error: entry or exit overlaps with the 42 pattern")
        return

    generator.add_42_pattern(entry, exit_cell)

    path_cells = generator.find_shortest_path(entry, exit_cell)
    if not path_cells:
        print("Error: no valid path from entry to exit")
        return
    path_directions = generator.path_to_directions(path_cells)

    generator.save_hex(
        config["output_file"],
        entry,
        exit_cell,
        path_directions,
    )

    try:
        run_interactive(generator, entry, exit_cell, path_cells)
    except curses.error as error:
        print(f"Warning: interactive mode could not start: {error}")


if __name__ == "__main__":
    main()
