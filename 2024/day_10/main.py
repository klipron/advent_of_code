import time

start = time.time()

import os
import ssl
from pathlib import Path
from typing import NamedTuple
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


class Point(NamedTuple):
    x: int
    y: int

    def get_next_points(self):
        yield Point(self.x + 1, self.y)
        yield Point(self.x - 1, self.y)
        yield Point(self.x, self.y + 1)
        yield Point(self.x, self.y - 1)


def solve(path: Path):
    grid: dict[Point, int] = {}
    for y, line in enumerate(path.open()):
        for x, num in enumerate(line.strip()):
            grid[Point(x, y)] = int(num)

    def walk_path(current_point: Point, starting_point: Point):
        if grid[current_point] == 9:
            yield (starting_point, current_point)
        for next_point in current_point.get_next_points():
            if next_point not in grid:
                continue
            if grid[next_point] == grid[current_point] + 1:
                yield from walk_path(next_point, starting_point)

    def walk_path_part2(path: tuple[Point, ...]):
        current_point = path[-1]
        if grid[current_point] == 9:
            yield path
        for next_point in current_point.get_next_points():
            if next_point not in grid:
                continue
            if grid[next_point] == grid[current_point] + 1:
                path += (next_point,)
                yield from walk_path_part2(path)

    part1_paths = set()
    part2_paths = []
    for point, num in grid.items():
        if num != 0:
            continue
        for path in walk_path(point, point):
            part1_paths.add(path)
        for path in walk_path_part2((point,)):
            part2_paths.append(path)
    show_answer(part=1, answer=len(part1_paths))
    show_answer(part=2, answer=len(part2_paths))


def get_input_file(year: int, day: int):
    if INPUT_FILE.exists():
        return
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    req = Request(url)
    req.add_header("Cookie", f"session={os.environ["AOC_SESSION"]}")
    context = ssl._create_unverified_context()
    try:
        resp: HTTPResponse = urlopen(req, context=context)
    except HTTPError as e:
        return print(e.read().decode())
    INPUT_FILE.write_bytes(resp.read(int(resp.getheader("Content-Length"))))


def show_answer(*, part: int, answer: int, test=False):
    print(
        f"{"Test Input " if test else ""}Answer Part {part}: {answer or ''}".ljust(50),
        "=" * 80,
        sep="\n",
    )


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    print(f"Advent of Code {year} Day {day}")
    print("=" * 80)
    get_input_file(year, day)
    if not INPUT_FILE.exists():
        return
    if TEST_FILE.exists():
        solve(TEST_FILE)
    solve(INPUT_FILE)


if __name__ == "__main__":
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
