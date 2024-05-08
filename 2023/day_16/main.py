from pathlib import Path
from datetime import date
from typing import Callable
from enum import Enum, auto
from http.client import HTTPResponse
from urllib.request import urlopen, Request

KEY_FILE = Path("key.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")
TEST_FILE = Path(__file__).with_name("test.txt")


def get_input_file(advent_date: date):
    if INPUT_FILE.exists():
        return
    url = f"https://adventofcode.com/{advent_date.year}/day/{advent_date.day}/input"
    req = Request(url)
    req.add_header("Cookie", f"session={KEY_FILE.read_text()}")
    resp: HTTPResponse = urlopen(req)
    INPUT_FILE.write_bytes(resp.read(int(resp.getheader("Content-Length"))))


Position = tuple[int, int]


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Beam:
    def __init__(self, start_pos: Position, direction: Direction) -> None:
        self.current_pos = start_pos
        self.direction = direction
        self.stopped = False

    def stop(self):
        self.stopped = True

    def move(self):
        x, y = self.current_pos
        if self.direction == Direction.UP:
            self.current_pos = (x, y - 1)
        elif self.direction == Direction.DOWN:
            self.current_pos = (x, y + 1)
        elif self.direction == Direction.LEFT:
            self.current_pos = (x - 1, y)
        elif self.direction == Direction.RIGHT:
            self.current_pos = (x + 1, y)

    def interact_with_tile(
        self, tile: str, add_beam: Callable[[Position, Direction], None]
    ):
        assert len(tile) == 1
        if tile == ".":
            return
        elif tile == "-":
            if self.direction in (Direction.LEFT, Direction.RIGHT):
                return
            if self.direction in (Direction.UP, Direction.DOWN):
                self.stop()
                for direction in Direction.LEFT, Direction.RIGHT:
                    add_beam(self.current_pos, direction)
        elif tile == "|":
            if self.direction in (Direction.UP, Direction.DOWN):
                return
            if self.direction in (Direction.LEFT, Direction.RIGHT):
                self.stop()
                for direction in Direction.UP, Direction.DOWN:
                    add_beam(self.current_pos, direction)
        elif tile == "/":
            self.direction = {
                Direction.UP: Direction.RIGHT,
                Direction.DOWN: Direction.LEFT,
                Direction.LEFT: Direction.DOWN,
                Direction.RIGHT: Direction.UP,
            }[self.direction]
        elif tile == "\\":
            self.direction = {
                Direction.UP: Direction.LEFT,
                Direction.DOWN: Direction.RIGHT,
                Direction.LEFT: Direction.UP,
                Direction.RIGHT: Direction.DOWN,
            }[self.direction]


def get_grid(path: Path):
    data = path.read_text()
    lines = data.splitlines()
    grid: dict[Position, str] = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            grid[(x, y)] = char
    return grid


def get_energized_tiles(grid: dict[Position, str], start_pos: Position):
    GRID_WIDTH = max(x for x, _ in grid)
    GRID_HEIGHT = max(y for _, y in grid)
    energized_tiles: set[Position] = set()
    paths_travelled: set[(Position, Direction)] = set()
    beams: list[Beam] = [Beam(start_pos, Direction.RIGHT)]
    add_beam = lambda position, direction: beams.append(Beam(position, direction))
    out_of_bounds = lambda x, y: x < 0 or y < 0 or x > GRID_WIDTH or y > GRID_HEIGHT
    while beams:
        beam = beams.pop(0)
        while True:
            if beam.stopped:
                break
            if out_of_bounds(*beam.current_pos):
                break
            if (beam.current_pos, beam.direction) in paths_travelled:
                break
            energized_tiles.add(beam.current_pos)
            paths_travelled.add((beam.current_pos, beam.direction))
            beam.interact_with_tile(grid[beam.current_pos], add_beam)
            if not beam.stopped:
                beam.move()
    return len(energized_tiles)


def part1(path: Path):
    grid = get_grid(path)
    return get_energized_tiles(grid, (0, 0))


def part2(path: Path):
    grid = get_grid(path)
    GRID_WIDTH = max(x for x, _ in grid)
    GRID_HEIGHT = max(y for _, y in grid)
    max_energized_tiles = 0
    for x, y in grid:
        if not (x in (0, GRID_WIDTH) or y in (0, GRID_HEIGHT)):
            continue
        energized_tiles = get_energized_tiles(grid, (x, y))
        if energized_tiles > max_energized_tiles:
            max_energized_tiles = energized_tiles
    return max_energized_tiles


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
    file = INPUT_FILE
    print(f"Answer Part 1: {part1(file) or ''}")
    print("=" * 80)
    print(f"Answer Part 2: {part2(file) or ''}")
    print("=" * 80)


if __name__ == "__main__":
    main()
