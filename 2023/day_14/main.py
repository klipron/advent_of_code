from enum import Enum, auto
from pathlib import Path
from datetime import date
from http.client import HTTPResponse
from urllib.request import urlopen, Request

KEY_FILE = Path("key.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")
TEST_FILE = Path(__file__).with_name("test.txt")

Platform = tuple[tuple[str, ...]]


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


def get_input_file(advent_date: date):
    if INPUT_FILE.exists():
        return
    url = f"https://adventofcode.com/{advent_date.year}/day/{advent_date.day}/input"
    req = Request(url)
    req.add_header("Cookie", f"session={KEY_FILE.read_text()}")
    resp: HTTPResponse = urlopen(req)
    INPUT_FILE.write_bytes(resp.read(int(resp.getheader("Content-Length"))))


def get_platform(path: Path) -> Platform:
    return tuple(
        tuple(c for c in line.strip()) for line in path.read_text().splitlines()
    )


def tilt_line(split_line: tuple[str, ...], *, reverse=False):
    line = "".join(reversed(split_line) if reverse else split_line)
    line = "#".join(
        "O" * part.count("O") + "." * (len(part) - part.count("O"))
        for part in line.split("#")
    )
    new_split_line = tuple(c for c in line)
    return tuple(reversed(new_split_line)) if reverse else new_split_line


def tilt_platform(platform: Platform, direction: Direction):
    if direction in (Direction.NORTH, Direction.SOUTH):
        return tuple(
            zip(
                *(
                    tilt_line(column, reverse=direction == Direction.SOUTH)
                    for column in zip(*platform)
                )
            )
        )
    if direction in (Direction.EAST, Direction.WEST):
        return tuple(
            tilt_line(row, reverse=direction == Direction.EAST) for row in platform
        )


def calculate_column_load(column: tuple[str, ...]):
    load = 0
    for i, c in enumerate(reversed(column), start=1):
        if c == "O":
            load += i
    return load


def calculate_platform_load(platform: Platform):
    return sum(calculate_column_load(column) for column in zip(*platform))


def part1(path: Path):
    if not path.exists():
        return
    platform = get_platform(path)
    platform = tilt_platform(platform, Direction.NORTH)
    return calculate_platform_load(platform)


def part2(path: Path):
    if not path.exists():
        return

    platform = get_platform(path)

    loads = set()
    load_pattern: list[int] = []
    first_idx = 0
    last_idx = 0
    i = 1
    while True:
        for direction in (
            Direction.NORTH,
            Direction.WEST,
            Direction.SOUTH,
            Direction.EAST,
        ):
            platform = tilt_platform(platform, direction)
        load = calculate_platform_load(platform)
        if len(load_pattern) > 1 and load_pattern[0] == load:
            break
        if not load_pattern:
            first_idx = i
        if not load_pattern or (load in loads and i == last_idx + 1):
            last_idx = i
            load_pattern.append(load)
        else:
            load_pattern = []
            last_idx = 0
        loads.add(load)
        i += 1
    return load_pattern[(1_000_000_000 - first_idx) % len(load_pattern)]


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    advent_date = date(year, 12, day)
    print(f"Advent of Code Day {advent_date.day}")
    print("=" * 80)
    if advent_date > date.today():
        print(
            f"Today's challenge is not ready as yet please try again in {advent_date - date.today()}"
        )
        return
    get_input_file(advent_date)
    file = TEST_FILE
    print(f"Answer Part 1: {part1(file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
