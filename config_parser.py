"""Configuration parser for the A-Maze-ing project.

The configuration file contains one ``KEY=VALUE`` pair per line. Empty
lines and lines starting with ``#`` are ignored.
"""

from typing import Any


def parse_int(key: str, value: str) -> int:
    """Convert the value of a configuration key into an integer.

    Args:
        key: Name of the key, used in the error message.
        value: Text to convert, for example ``"20"``.

    Returns:
        The integer value.

    Raises:
        ValueError: If the value is not an integer.
    """
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{key} must be an integer, got '{value}'") from None


def parse_coordinates(key: str, value: str) -> tuple[int, int]:
    """Convert text like ``"0,0"`` into a tuple of two integers.

    Args:
        key: Name of the key, used in the error message.
        value: Coordinates written as ``x,y``.

    Returns:
        The coordinates as ``(x, y)``.

    Raises:
        ValueError: If the text is not two integers separated by a comma.
    """
    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError(f"{key} must be written as x,y, got '{value}'")

    x = parse_int(f"{key} x", parts[0].strip())
    y = parse_int(f"{key} y", parts[1].strip())

    return x, y


def parse_bool(value: str) -> bool:
    """Convert the text ``True`` or ``False`` into a boolean.

    Args:
        value: Either ``"True"`` or ``"False"``.

    Returns:
        The boolean value.

    Raises:
        ValueError: If the text is neither ``"True"`` nor ``"False"``.
    """
    if value == "True":
        return True
    if value == "False":
        return False

    raise ValueError(f"Invalid boolean value: {value}")


def validate_config(config: dict[str, Any]) -> None:
    """Check that the configuration values describe a valid maze.

    Args:
        config: The parsed configuration, as returned by ``load_config``.

    Raises:
        ValueError: If the size is not between 1 and 500, if the entry and
            the exit are equal, or if one of them is outside the maze.
    """
    width = config["width"]
    height = config["height"]
    entry = config["entry"]
    exit_point = config["exit"]

    if not (0 < width <= 500 and 0 < height <= 500):
        raise ValueError("WIDTH and HEIGHT must be between 1 and 500")

    entry_x, entry_y = entry
    exit_x, exit_y = exit_point

    if entry == exit_point:
        raise ValueError("ENTRY and EXIT must be different")

    if not 0 <= entry_x < width or not 0 <= entry_y < height:
        raise ValueError("ENTRY must be inside the maze")

    if not 0 <= exit_x < width or not 0 <= exit_y < height:
        raise ValueError("EXIT must be inside the maze")


def load_config(filename: str) -> dict[str, Any]:
    """Read, parse and validate the configuration file.

    Args:
        filename: Path of the configuration file.

    Returns:
        A dictionary with the keys ``width``, ``height``, ``entry``,
        ``exit``, ``output_file``, ``perfect`` and ``seed``. ``entry`` and
        ``exit`` are ``(x, y)`` tuples.

    Raises:
        OSError: If the file cannot be read.
        KeyError: If a mandatory key is missing.
        ValueError: If a line or a value is invalid.
    """
    raw_config: dict[str, str] = {}

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(f"Invalid config line: {line}")

            key, value = line.split("=", 1)
            raw_config[key.strip()] = value.strip()

    config: dict[str, Any] = {
        "width": parse_int("WIDTH", raw_config["WIDTH"]),
        "height": parse_int("HEIGHT", raw_config["HEIGHT"]),
        "entry": parse_coordinates("ENTRY", raw_config["ENTRY"]),
        "exit": parse_coordinates("EXIT", raw_config["EXIT"]),
        "output_file": raw_config["OUTPUT_FILE"],
        "perfect": parse_bool(raw_config["PERFECT"]),
        "seed": parse_int("SEED", raw_config.get("SEED", "0")),
    }

    validate_config(config)

    return config
