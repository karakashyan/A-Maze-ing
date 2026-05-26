"""Configuration parser for the A-Maze-ing project."""


from typing import Any


def parse_coordinates(value: str) -> tuple[int, int]:
    """Convert text like '0,0' into a tuple of two integers."""
    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError(f"Invalid coordinates: {value}")

    x = int(parts[0])
    y = int(parts[1])

    return x, y


def parse_bool(value: str) -> bool:
    """Convert text True or False into a boolean."""
    if value == "True":
        return True
    if value == "False":
        return False

    raise ValueError(f"Invalid boolean value: {value}")


def validate_config(config: dict[str, Any]) -> None:
    """Validate maze configuration values."""
    width = config["width"]
    height = config["height"]
    entry = config["entry"]
    exit_point = config["exit"]

    if width <= 0:
        raise ValueError("WIDTH must be greater than 0")

    if height <= 0:
        raise ValueError("HEIGHT must be greater than 0")

    entry_x, entry_y = entry
    exit_x, exit_y = exit_point

    if entry == exit_point:
        raise ValueError("ENTRY and EXIT must be different")

    if not 0 <= entry_x < width or not 0 <= entry_y < height:
        raise ValueError("ENTRY must be inside the maze")

    if not 0 <= exit_x < width or not 0 <= exit_y < height:
        raise ValueError("EXIT must be inside the maze")


def load_config(filename: str) -> dict[str, Any]:
    """Read and parse the configuration file."""
    raw_config: dict[str, str] = {}

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Invalid config line: {line}")

            key, value = line.split("=", 1)
            raw_config[key] = value

    config: dict[str, Any] = {
        "width": int(raw_config["WIDTH"]),
        "height": int(raw_config["HEIGHT"]),
        "entry": parse_coordinates(raw_config["ENTRY"]),
        "exit": parse_coordinates(raw_config["EXIT"]),
        "output_file": raw_config["OUTPUT_FILE"],
        "perfect": parse_bool(raw_config["PERFECT"]),
        "seed": int(raw_config.get("SEED", "0")),
    }

    validate_config(config)

    return config
