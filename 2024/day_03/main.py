import os
import re
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


def get_substrings(data: str, *, start=0, do=True):
    if start == -1:
        return
    if do:
        idx = data.find("don't()", start)
        yield data[start:idx]
        yield from get_substrings(data, start=idx, do=False)
    else:
        idx = data.find("do()", start)
        yield from get_substrings(data, start=idx, do=True)


def get_substrings_v2(data: str):
    idx = start = 0
    do = True
    while idx != -1:
        if do:
            idx = data.find("don't()", start)
            yield data[start:idx]
        else:
            idx = data.find("do()", start)
        start = idx
        do = not do


def get_answers(path: Path, part1: Callable[[Any], None], part2: Callable[[Any], None]):
    data = path.read_text()
    get_total = lambda text: sum(
        (int(x) * int(y)) for x, y in re.findall(r"mul\((\d+),(\d+)\)", text)
    )
    part1(get_total(data))
    part2(sum(get_total(substring) for substring in get_substrings_v2(data)))


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