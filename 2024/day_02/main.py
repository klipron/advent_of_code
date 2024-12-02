import os
import ssl
import time
from pathlib import Path
from typing import Callable, Any
from urllib.error import HTTPError
from http.client import HTTPResponse
from urllib.request import urlopen, Request

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


def is_safe(*levels: int):
    diffs = tuple(y - x for x, y in zip(levels, levels[1:]))
    if not (all(x < 0 for x in diffs) or all(x > 0 for x in diffs)):
        return False
    if any(abs(x) > 3 for x in diffs):
        return False
    return True


def get_answers(path: Path, part1: Callable[[Any], None], part2: Callable[[Any], None]):
    reports = (tuple(map(int, x.strip().split())) for x in path.open().readlines())
    safe = 0
    unsafe_to_safe = 0
    for levels in reports:
        if is_safe(*levels):
            safe += 1
            continue
        for i in range(len(levels)):
            if is_safe(*(x for idx, x in enumerate(levels) if idx != i)):
                unsafe_to_safe += 1
                break
    part1(safe)
    part2(safe + unsafe_to_safe)


def main():
    day = int(Path(__file__).parent.name.split("_")[1])
    year = int(Path(__file__).parent.parent.name)
    print(f"Advent of Code {year} Day {day}")
    print("=" * 80)
    get_input_file(year, day)
    if not INPUT_FILE.exists():
        return
    part1 = lambda x: print(f"Answer Part 1: {x or ''}", "=" * 80, sep="\n")
    part2 = lambda x: print(f"Answer Part 2: {x or ''}", "=" * 80, sep="\n")
    get_answers(INPUT_FILE, part1, part2)


if __name__ == "__main__":
    start = time.time()
    main()
    print(
        f"Completed execution of {Path(__file__).name} in {time.time()-start:.3f} seconds."
    )
