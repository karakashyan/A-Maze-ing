"""Main entry point for the A-Maze-ing project."""

import sys
from config_parser import load_config
from maze_generator import MazeGenerator


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

    print("Config loaded successfully:")
    print(config)

    generator = MazeGenerator(
        width=config["width"],
        height=config["height"],
        seed=config["seed"],
    )

    # generator.remove_wall_between((0, 0), (1, 0))
    # generator.print_debug()
    # print(generator.get_neighbors((0, 0)))
    # print(generator.get_neighbors((1, 1)))
    generator.generate()
    print(generator.maze_to_hex_lines())
    # generator.print_debug()
    entry_x, entry_y = config["entry"]
    exit_x, exit_y = config["exit"]

    entry = (entry_y, entry_x)
    exit_cell = (exit_y, exit_x)
    path_cells = generator.find_shortest_path(entry, exit_cell)
    path_directions = generator.path_to_directions(path_cells)
    generator.save_hex(
        config["output_file"], entry, exit_cell, path_directions)


if __name__ == "__main__":
    main()
