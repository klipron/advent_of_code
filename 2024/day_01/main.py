import os
import ssl
import time
from pathlib import Path
from typing import Callable, Any
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request
from collections import Counter, defaultdict

TEST_FILE = Path(__file__).with_name("test.txt")
INPUT_FILE = Path(__file__).with_name("input.txt")


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


def get_answers(path: Path, part1: Callable[[Any], None], part2: Callable[[Any], None]):
    lines = path.open().readlines()
    lists = tuple(map(sorted, zip(*(map(int, line.strip().split()) for line in lines))))

    part1(sum(abs(x - y) for x, y in zip(*map(sorted, lists))))  # Part 1 Option 1
    part1(sum(abs(int.__sub__(*x)) for x in zip(*lists)))

    left, right = lists

    part2(
        sum(l * sum(1 for r in right if r == l) for l in left)
    )  # Part 2 Option 1: Very Slow
    part2(sum(l * right.count(l) for l in left))  # Part 2 Option 2

    # counter = defaultdict(int)  # Custom Counter Implementation
    # for r in right:
    #     counter[r] += 1
    counter = Counter(right)
    part2(sum(l * counter.get(l, 0) for l in left))


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    print(f"Advent of Code {year} Day {day}")
    print("=" * 80)
    get_input_file(year, day)
    path = INPUT_FILE
    if not path.exists():
        return
    part1 = lambda x: print(f"Answer Part 1: {x or ''}", "=" * 80, sep="\n")
    part2 = lambda x: print(f"Answer Part 2: {x or ''}", "=" * 80, sep="\n")
    get_answers(path, part1, part2)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
