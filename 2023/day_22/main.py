import time
import string
from pathlib import Path
from datetime import date
from typing import NamedTuple
from collections import defaultdict
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


class Point(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"


class Brick(NamedTuple):
    key: int
    start: Point
    end: Point

    def __repr__(self) -> str:
        return f"Brick(key={self.key}, start={self.start}, end={self.end})"

    def iter_points(self):
        for x in range(self.start.x, self.end.x + 1):
            for y in range(self.start.y, self.end.y + 1):
                yield Point(x, y)


def get_levels(path: Path):
    levels: dict[int, set[Brick]] = defaultdict(set)
    lines = path.open().readlines()
    for key, line in enumerate(lines):
        start, end = line.strip().split("~")
        x, y, z = list(map(int, start.split(",")))
        _x, _y, _z = list(map(int, end.split(",")))
        for i in range(z, _z + 1):
            levels[i].add(
                Brick(
                    (
                        string.ascii_uppercase[key]
                        if len(lines) < len(string.ascii_uppercase)
                        else str(key)
                    ),
                    Point(x, y),
                    Point(_x, _y),
                )
            )
    for i in range(1, max(levels) + 1):
        if i not in levels:
            levels[i] = set()
    return levels


def get_level_points(levels: dict[int, set[Brick]]):
    max_point = max(brick.end for bricks in levels.values() for brick in bricks)
    level_points: set[Point] = set()
    for x in range(max_point[0] + 1):
        for y in range(max_point[1] + 1):
            level_points.add(Point(x, y))
    return level_points


def shift_bricks_down(levels: dict[int, set[Brick]]):
    level_points = get_level_points(levels)
    for level in range(2, max(levels) + 1):
        for i in [x + 1 for x in range(level)][::-1]:
            if i - 1 == 0:
                continue
            empty_space = level_points - set(
                point for brick in levels[i - 1] for point in brick.iter_points()
            )
            move_bricks: list[Brick] = []
            for brick in levels[i]:
                if all(x in empty_space for x in brick.iter_points()):
                    levels[i - 1].add(brick)
                    move_bricks.append(brick)
            for brick in move_bricks:
                levels[i].remove(brick)
    return levels


def get_brick_dependencies(levels: dict[int, set[Brick]]):
    dependencies: dict[Brick, set[Brick]] = defaultdict(set)
    for z in sorted(levels, reverse=True):
        for brick in levels[z]:
            lower_level = levels[z - 1]
            if brick in lower_level:
                continue
            for lower_brick in lower_level:
                if set(brick.iter_points()) & set(lower_brick.iter_points()):
                    dependencies[brick].add(lower_brick)
    return dependencies


def part1(path: Path):
    levels = shift_bricks_down(get_levels(path))
    all_points = get_level_points(levels)

    can_be_removed = set()
    for z, bricks in sorted(levels.items(), key=lambda x: x[0]):
        for brick in bricks:
            empty_space = all_points - set(
                point
                for _brick in bricks
                for point in _brick.iter_points()
                if brick != _brick
            )
            upper_level = levels[z + 1]
            if brick in upper_level:
                continue
            for upper_brick in upper_level:
                if all(point in empty_space for point in upper_brick.iter_points()):
                    break
            else:
                can_be_removed.add(brick)
    return len(can_be_removed)


def part2(path: Path):
    levels = shift_bricks_down(get_levels(path))
    brick_dependencies = get_brick_dependencies(levels)

    starting_bricks: dict[Brick, set[Brick]] = defaultdict(set)
    for brick, dependencies in brick_dependencies.items():
        if len(dependencies) != 1:
            continue
        key = list(dependencies)[0]
        starting_bricks[key].add(brick)

    for brick in starting_bricks:
        while True:
            length = len(starting_bricks[brick])
            for b, dependencies in brick_dependencies.items():
                if all(d in starting_bricks[brick] for d in dependencies):
                    starting_bricks[brick].add(b)
            if length == len(starting_bricks[brick]):
                break

    return sum((len(x) for x in starting_bricks.values()))


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
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
