import os
import ssl
import time
from pathlib import Path
from urllib.error import HTTPError
from typing import Self, NamedTuple
from collections import defaultdict
from http.client import HTTPResponse
from urllib.request import urlopen, Request

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


class Point(NamedTuple):
    x: int
    y: int

    def get_next_point(self, end_point: Self):
        dx = end_point.x - self.x
        dy = end_point.y - self.y
        return Point(end_point.x + dx, end_point.y + dy)


def solve(path: Path, test=False):
    grid: dict[Point, str] = {}
    for y, line in enumerate(path.open()):
        for x, char in enumerate(line.strip()):
            grid[Point(x, y)] = char

    antennas = defaultdict(list[Point])
    for point, char in grid.items():
        if char == ".":
            continue
        antennas[char].append(point)

    antenna_points: list[tuple[Point, Point]] = []
    for points in antennas.values():
        for point in points:
            for other_point in points:
                if point == other_point:
                    continue
                antenna_points.append((point, other_point))

    part1_antinodes = set()
    part2_antinodes = set()
    for point, other_point in antenna_points:
        part2_antinodes.update((point, other_point))
        part1 = True
        while True:
            next_point = point.get_next_point(other_point)
            if next_point not in grid:
                break
            if part1:
                part1_antinodes.add(next_point)
                part1 = False
            part2_antinodes.add(next_point)
            point, other_point = other_point, next_point
    show_answer(part=1, answer=len(part1_antinodes), test=test)
    show_answer(part=2, answer=len(part2_antinodes), test=test)


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
        solve(TEST_FILE, test=True)
    solve(INPUT_FILE)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
