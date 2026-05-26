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
    print(generator.get_neighbors((0, 0)))
    print(generator.get_neighbors((1, 1)))


if __name__ == "__main__":
    main()
