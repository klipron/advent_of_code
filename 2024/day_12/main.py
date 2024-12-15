import time
from typing import NamedTuple

start = time.time()

import os
import ssl
from pathlib import Path
from collections import defaultdict
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


class Point(NamedTuple):
    x: int
    y: int

    def get_perimeter_points(self):
        yield Point(self.x + 1, self.y)
        yield Point(self.x - 1, self.y)
        yield Point(self.x, self.y + 1)
        yield Point(self.x, self.y - 1)


def solve(path: Path, test=False):
    grid = {
        Point(x, y): char
        for y, line in enumerate(path.open())
        for x, char in enumerate(line.strip())
    }

    def get_region(point: Point, seen: set[Point] | None = None):
        if seen is None:
            yield point
            seen = {point}
        for perimeter_point in point.get_perimeter_points():
            if perimeter_point not in grid:
                continue
            if perimeter_point in seen:
                continue
            seen.add(perimeter_point)
            if grid[point] != grid[perimeter_point]:
                continue
            yield perimeter_point
            yield from get_region(perimeter_point, seen)

    def get_region_perimeter(region: set[Point]):
        perimeter_points: list[Point] = []
        for point in region:
            for perimeter_point in point.get_perimeter_points():
                if perimeter_point not in grid:
                    perimeter_points.append(perimeter_point)
                    continue
                if grid[point] == grid[perimeter_point]:
                    continue
                perimeter_points.append(perimeter_point)
        return perimeter_points

    regions: list[set[Point]] = []
    seen: set[Point] = set()
    for point in grid:
        if point in seen:
            continue
        region = set(get_region(point))
        regions.append(region)
        seen.update(region)

    total = sum(len(x) * len(get_region_perimeter(x)) for x in regions)
    show_answer(part=1, answer=total)


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
    # solve(INPUT_FILE)


if __name__ == "__main__":
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
