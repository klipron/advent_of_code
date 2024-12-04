import os
import ssl
import time
from pathlib import Path
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request
from typing import Callable, Any, NamedTuple
from collections import Counter

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


class Answer(NamedTuple):
    part: int
    value: Any


class Point(NamedTuple):
    x: int
    y: int


Grid = dict[Point, str]


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


def get_grid(path: Path) -> Grid:
    grid: Grid = {}
    for y, row in enumerate(path.open().read().splitlines()):
        for x, column in enumerate(row):
            grid[Point(x, y)] = column
    return grid


def get_word_points(start_point: Point, *, word_len=4, diagonal_only=False):
    yield (Point(start_point.x + i, start_point.y - i) for i in range(word_len))
    yield (Point(start_point.x + i, start_point.y + i) for i in range(word_len))
    yield (Point(start_point.x - i, start_point.y - i) for i in range(word_len))
    yield (Point(start_point.x - i, start_point.y + i) for i in range(word_len))
    if diagonal_only:
        return
    yield (Point(start_point.x, start_point.y + i) for i in range(word_len))
    yield (Point(start_point.x, start_point.y + i) for i in range(0, -word_len, -1))
    yield (Point(start_point.x + i, start_point.y) for i in range(word_len))
    yield (Point(start_point.x + i, start_point.y) for i in range(0, -word_len, -1))


def search_for_word(grid: Grid, word: str, *, diagonal_only=False):
    for point, char in grid.items():
        if char != word[0]:
            continue
        for points in (
            tuple(x)
            for x in get_word_points(
                point, word_len=len(word), diagonal_only=diagonal_only
            )
        ):
            if "".join((grid.get(x, "") for x in points)) == word:
                yield points


def solve(path: Path, show_answer: Callable[[Answer], None]):
    grid = get_grid(path)

    show_answer(Answer(1, sum(1 for _ in search_for_word(grid, "XMAS"))))
    counter = Counter(x[1] for x in search_for_word(grid, "MAS", diagonal_only=True))
    show_answer(Answer(2, sum(1 for x in counter.values() if x == 2)))


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    print(f"Advent of Code {year} Day {day}")
    print("=" * 80)
    get_input_file(year, day)
    if not INPUT_FILE.exists():
        return
    show_answer: Callable[[Answer], None] = lambda answer: print(
        f"Answer Part {answer.part}: {answer.value or ''}", "=" * 80, sep="\n"
    )
    solve(INPUT_FILE, show_answer)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
